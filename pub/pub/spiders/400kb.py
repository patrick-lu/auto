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
from time import time

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
	if not self.tt or self.tt=="":
		print "pub: 400k no item to publish"
		return
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
	self.tt["pub_progress"]="1"
	self.tt["pub_time"]=int(time())
		
	#threads_db.save(tt)
	saveItem(self.tt)
	#inspect_response(response)
	return self.adv_request();

    def adv_request(self):
	adv_link="http://adf.ly";
	return Request(adv_link,callback=self.login)
	#adv_link="http://www.linkbucks.com/Default.aspx"
	#return Request(adv_link,callback=self.linkbucks_login)

    def linkbucks_login(self, response):
	name = settings["linkbucks_name"]
	pw = settings["linkbucks_pass"]
	return [FormRequest.from_response(response,
                    formdata={'ctl00$LeftMenuBar$ctl00$Username': name, 'ctl00$LeftMenuBar$ctl00$Password': pw},
                    callback=self.linkbucks_after_login)]

    def linkbucks_after_login(self, response):
	if(response.url.find("lup2k")>-1):
		#inspect_response(response)
		''' save to adf.ly'''
		url = "http://www.linkbucks.com/CreateLinks/Single/"
		return Request(url,callback=self.linkbucks_submit)
	else:
		self.log("ERROR: failed to login linkbucks")
		return
    def linkbucks_submit(self, response):
	 return [FormRequest.from_response(response,
                    formdata={'ctl00$MainBody$ctl02$txtOrgLink': self.tt["publish"]["btfile"],
			'ctl00$MainBody$ctl02$drpContentType': '2',
			'ctl00$MainBody$ctl02$drpAdType':'2',
			'ctl00$MainBody$ctl02$drpAliasURL':'51',  #linkbabes.com 
			},
                    callback=self.linkbucks_get_short)]


    def linkbucks_get_short(self, response):
	inspect_response(response)
	self.tt["publish"]["url"]=response.body;
	
    

    def login(self, response):
	name = settings["adfly_name"]
	pw = settings["adfly_pass"]
	return [FormRequest.from_response(response,
                    formdata={'email': name, 'password': pw},
                    callback=self.after_login)]

    def after_login(self, response):
	if(response.url.find("adf.ly/publisher")>-1):
		#inspect_response(response)
		''' save to adf.ly'''
		url ="http://adf.ly/shrink.php?url="+self.tt["publish"]["btfile"]+"&x=0.5941863050684333&advert_type=1&custom_name=&logged=1&domain=1"
		return Request(url,callback=self.get_short)
	else:
		self.log("ERROR: failed to login adf.ly")


    def get_short(self, response):
	self.tt["publish"]["url"]=response.body;
#	inspect_response(response)
	saveItem(self.tt)
	img_share_link = "http://www.imageporter.com/login.html"
	#return Request(img_share_link,callback=self.imgShare_login)
	#img_share_link = "http://shareimage.org/"
	'''shareimge worked, but now cant upload because of multi-files name'''
	#img_share_link = "http://shareimage.org/users.php?act=login&return=aHR0cDovL3NoYXJlaW1hZ2Uub3JnL3VzZXJzLnBocD9hY3Q9bG9nb3V0&lb_div=login_lightbox"
	#return Request(img_share_link,callback=self.shareimage_login)
	lulzimg_link = "http://lulzimg.com"
	return Request(lulzimg_link, callback = self.lulzimg_post,dont_filter=True)

    def lulzimg_post(self, response):
	basedir = settings['IMAGES_STORE']
	params={}
	params['uploadtype']='image'
	params['submit']=''
	self.tt['publish']['imgs']=[]
	for img in self.tt['images']:
		key=img[1]
		path_comps= key.split('/')
		filename=os.path.join(basedir, *path_comps)
		self.log( filename);
		#inspect_response(response)
		params['image']=open(filename,'rb')
		datagen, headers = multipart_encode(params)
		upload_url = "http://lulzimg.com/upload.php"
		req = urllib2.Request(upload_url, datagen, headers)
		result = urllib2.urlopen(req)
		content=result.read()
		#print content
		p = re.compile(r'imagecode1(.)+value="(http://\S+)"')
       		match=p.search(content);
 	        self.log( match.group(2))
        	if match:
                	self.tt['publish']['imgs'].append(match.group(2))
                	saveItem(self.tt)
        	else:
                	self.log("ERROR: failed to upload image")
        return;

    def shareimage_login(self, response):
	name = settings["shareimage_name"]
	pw = settings["shareimage_pass"]
	return [FormRequest.from_response(response,
                    formdata={'username': name, 'password': pw},
                    callback=self.after_shareimage_login)]

    def after_shareimage_login(self, response):
	#inspect_response(response)
	if(response.body.find("You have been successfully logged in")>-1):
		tmp = response.headers['Set-Cookie']
		cookie="";
		p=re.compile(r'mmh_user_session=\S+')
		match = p.search(tmp);
		if(match) :
			cookie=match.group(0)		
			url = "http://shareimage.org/index.php"
			self.tt['publish']['imgs']=[]
			for img in self.tt['images']:
				img_key = img[1];
				request=Request(url,callback=self.shareimage_post)
				request.meta['cookie']=cookie
				request.meta['key']=img_key
				yield request
		else:
			self.log("ERROR: failed to login shareimage.org")
	else:
		self.log("ERROR: failed to login shareimage.org")

    def shareimage_post(self, response):
	#register_openers()
	params={};
	basedir = settings['IMAGES_STORE']
	key=response.meta['key']
	path_comps= key.split('/')
	filename=os.path.join(basedir, *path_comps)
	print filename;
	inspect_response(response)
	params["userfile[]"]=open(filename,"rb")
	params["private_upload"]=0
	datagen, headers = multipart_encode(params)
	upload_url = "http://shareimage.org/upload.php"
	req = urllib2.Request(upload_url, datagen, headers)
	print response.meta['cookie']
	req.add_header('Cookie',response.meta['cookie'])
	result = urllib2.urlopen(req)
	content=result.read()
	print content
	response["meta"]['tttt']=content
	inspect_response(response)
	p = re.compile(r'value="(http://\S+)"')
	match=p.search(content);
	print match.group(1)
	if match:		
		self.tt['publish']['imgs'].append(match.group(1))
		saveItem(self.tt)	
	else:
		self.log("ERROR: failed to upload image")
#	inspect_response(response)
	return;

    def imgShare_login(self, response):
	name = settings["imageporter_name"]
	pw = settings["imageporter_pass"]
	return [FormRequest.from_response(response,
                    formdata={'login': name, 'password': pw},
                    callback=self.after_imgShare_login)]

    def after_imgShare_login(self, response):
	if(response.url.find("imageporter.com/?op=my_files")>-1):
		url = "http://www.imageporter.com/"
		return Request(url,callback=self.post_imgs)
	else:
		self.log("ERROR: failed to login imageporter.com")


    def post_imgs(self, response):
	inspect_response(response)
