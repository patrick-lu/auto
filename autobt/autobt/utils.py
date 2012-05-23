from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from autobt.items import AutobtItem
from scrapy.shell import inspect_response
import urlparse

import re

def parse_bt(item):
	item["attach"]=[]
	#if not item['links']:
#		 return item;
	next_link="";
	order=[
		'adf.ly'
		]

	for key in order:
		for link in item['links']:
			if link.find(key) > 0:
				next_link=link;
				request = Request(next_link,callback=parse_bt_cb)
				request.meta['item'] = item;
				return request;
	return item;
	

def parse_bt_cb(response):
	next_link="";
	item = response.meta['item']
	if response.url.find("adf.ly") > -1:
		p = re.compile(r'(http://adf.ly/go/(\w|\/)+)')
		match = p.search(response.body)
		if match:
			next_link=match.group(1)
	elif response.url.find("400kb.com")>-1:
		#inspect_response(response)
		hxs = HtmlXPathSelector(response)
		code = hxs.select("//input[normalize-space(@name)='ref']/@value").extract()[0]
		url = hxs.select("//form[normalize-space(@name)='bbrules']/@action").extract()[0]
		absolute_link= urlparse.urljoin(response.url, url.strip())
		param={"ref":code}
		item['attach']=["post",absolute_link,param]
		
	if next_link:
		request = Request(next_link,callback=parse_bt_cb)
		request.meta['item'] = item;
		return request
	return item;

