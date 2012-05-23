from scrapy.spider import BaseSpider
from scrapy.shell import inspect_response
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.http import FormRequest

import os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from pymongo import Connection
from pub.utils import selectToPub
from pub.utils import saveItem
import re

class DmozSpider(BaseSpider):
    name = "400kb"
    #allowed_domains = ["400kb.com"]
    start_urls = [
	"http://www.400kb.com/upload.php"
    ]
    upload_url = "http://www.400kb.com/upload.php"

    
    def parse(self, response):
	hxs = HtmlXPathSelector(response)
	inputs=hxs.select("//form[normalize-space(@name)='form1']//input")
	params={};
	#conn = Connection()
	#db = conn.autobt
	#threads_db = db.threads
	#tt=threads_db.find_one();
	self.tt=selectToPub();
	for input in inputs:
		type=input.select("./@type").extract()[0]
		if type.find("hidden") > -1:
			name=input.select("./@name").extract()[0]
			val =input.select("./@value").extract()[0]
			params[name]=val;
		elif type.find("file") > -1:
			name=input.select("./@name").extract()[0]
			basedir = settings['BTFILES_STORE']
			key=self.tt['btfile']
			path_comps= key.split('/')
			filename=os.path.join(basedir, *path_comps)		
			val = open(filename,"rb")
			params[name]=val;
		

	register_openers()
	datagen, headers = multipart_encode(params)
	req = urllib2.Request(self.upload_url, datagen, headers)
	result = urllib2.urlopen(req)
	content=result.read()
	p = re.compile(r'http://www.400kb.com/go.php\?ref=(\w)+');
	content = content.encode('utf-8')
	match = p.search(content)
	if not "publish" in self.tt:
		self.tt["publish"]={}
	self.tt["publish"]["btfile"]=match.group(0);
		
	#threads_db.save(tt)
	saveItem(self.tt)
	#inspect_response(response)
	adv_link="http://adf.ly";
	return Request(adv_link,callback=self.login)

    def login(self, response):
	name = settings["adfly_name"]
	pw = settings["adfly_pass"]
	return [FormRequest.from_response(response,
                    formdata={'email': name, 'password': pw},
                    callback=self.after_login)]

    def after_login(self, response):
	if(response.url.find("adf.ly/publisher")>-1):
		#inspect_response(response)
		url ="http://adf.ly/shrink.php?url="+self.tt["publish"]["btfile"]+"&x=0.5941863050684333&advert_type=1&custom_name=&logged=1&domain=1"
		return Request(url,callback=self.get_short)
	else:
		self.log("ERROR: failed to login adf.ly")


    def get_short(self, response):
	self.tt["publish"]["adv"]=response.body;
#	inspect_response(response)
	saveItem(self.tt)
	return;
