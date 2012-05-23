from scrapy.spider import BaseSpider
from scrapy.shell import inspect_response
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings

import os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from pymongo import Connection
import re

class DmozSpider(BaseSpider):
    name = "400kb"
    allowed_domains = ["400kb.com"]
    start_urls = [
	"http://www.400kb.com/upload.php"
    ]
    upload_url = "http://www.400kb.com/upload.php"
    def parse(self, response):
	hxs = HtmlXPathSelector(response)
	inputs=hxs.select("//form[normalize-space(@name)='form1']//input")
	params={};
	conn = Connection()
	db = conn.autobt
	threads_db = db.threads
	tt=threads_db.find_one();
	for input in inputs:
		type=input.select("./@type").extract()[0]
		if type.find("hidden") > -1:
			name=input.select("./@name").extract()[0]
			val =input.select("./@value").extract()[0]
			params[name]=val;
		elif type.find("file") > -1:
			name=input.select("./@name").extract()[0]
			basedir = settings['BTFILES_STORE']
			key=tt['btfile']
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
	tt["btfile_url"]= match.group(0);
	threads_db.save(tt)

	#inspect_response(response)
