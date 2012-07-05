from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from pymongo import Connection
from pymongo.database import Database
from autobt.items import AutobtItem
from scrapy.shell import inspect_response
import urlparse
from time import time
import re


def createNewThread(post):
	db_name=settings['DB_NAME']
	conn = Connection()
	db = Database(conn,db_name)
	threads_db = db.threads
	ex= threads_db.find_one({"url":post['url']})
	if not ex:
		post["grab_progress"]="0"
		post["reply"]={}
		post["grab_time"]=int(time())
		threads_db.insert(post)
		return True;
	return False;

	

def parseDetailFromContent(content):
	con={}
	colon =  u'\uff1a'
	tags={
	  u'\u5f71\u7247\u540d\u7a31':"name",
	  u'\u5f71\u7247\u540d\u79f0':"name",
	  u'\u5f71\u7247\u683c\u5f0f':"format",
	  u'\u5f71\u7247\u5927\u5c0f':"size",
	}
	
	for key in tags:
		index =content.find(key);
		if(index >0):
			name =content[index:]
			index = name.find("<br>")
			if(index <0 ):
				index = name.find("\t")
			if(index >0):
				name = name[0:index]
				index = name.find(colon)
				if(index > 0):
					con[tags[key]] = name[(index+1):]
				else:
					index = name.find(u":")
					if(index>0):
						con[key] = name[(index+1):]

	result={'level':len(con),"items":con}
	return result;


def parse_bt(item):
	item["attach"]=[]
	#if not item['links']:
#		 return item;
	next_link="";
	order=[
		'adf.ly',
		'mimima.com',
		'pidown.com',
		'jandown.com',
		]

	for key in order:
		for link in item['links']:
			if link.find(key) > 0:
				next_link=link;
				request = Request(next_link,callback=parse_bt_cb)
				request.meta['item'] = item;
				return request;
	for link in item['links']:
		if link[0]=='/':
			absolute_link= urlparse.urljoin(item['name'], link.strip())
			item['attach']=["get",absolute_link,'']
			return item;
	print "ERROR no bt download found"
	return item;
	

def parse_bt_cb(response):
	next_link="";
	item = response.meta['item']
	if response.url.find("adf.ly") > -1:
		p = re.compile(r'(http://adf.ly/go/(\w|\/)+)')
		match = p.search(response.body)
		if match:
			next_link=match.group(1)
		else:
			p = re.compile(r'(go/(\w|\/)+)')
			match = p.search(response.body)
			if match:
				next_link="http://adf.ly/"+match.group(1)
			else:
				print "ERROR: parse adf.ly link"
	elif response.url.find("400kb.com")>-1:
		#inspect_response(response)
		hxs = HtmlXPathSelector(response)
		code = hxs.select("//input[normalize-space(@name)='ref']/@value").extract()[0]
		url = hxs.select("//form[normalize-space(@name)='bbrules']/@action").extract()[0]
		absolute_link= urlparse.urljoin(response.url, url.strip())
		param={"ref":code}
		item['attach']=["post",absolute_link,param]
	elif response.url.find("pidown.com")>-1:
		#inspect_response(response)
		hxs = HtmlXPathSelector(response)
		code = hxs.select("//input[normalize-space(@name)='code']/@value").extract()[0]
		url = hxs.select("//form[normalize-space(@name)='bbrules']/@action").extract()[0]
		absolute_link= urlparse.urljoin(response.url, url.strip())
		param={"code":code}
		item['attach']=["post",absolute_link,param]
		
	if next_link:
		request = Request(next_link,callback=parse_bt_cb)
		request.meta['item'] = item;
		return request
	return item;

