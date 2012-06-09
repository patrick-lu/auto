from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from autobt.items import AutobtItem
from scrapy.shell import inspect_response
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.conf import settings
from pymongo import Connection
from scrapy.conf import settings
from pymongo.database import Database
import urlparse
import datetime

from autobt.utils import parse_bt
from autobt.utils import parseDetailFromContent
from autobt.utils import createNewThread

from time import sleep

class CrawlSpider(CrawlSpider):
    name = 'xiaav'
    classify='1'
    db_name=settings['DB_NAME']
    conn = Connection()
    db = Database(conn,db_name)
    threads_db = db.threads

    
    #download_delay =10
    #randomize_download_delay=True;
    #allowed_domains = ['www.google.com']
    start_urls = [
                     'http://108.170.27.83/forum.php',
		     #'http://108.170.27.83/forum-2-1.html',
		     #'http://108.170.27.83/forum-2-2.html',
                 ]
    parse_urls = [
		     'http://108.170.27.83/forum-2-1.html',
		    # 'http://108.170.27.83/forum-2-2.html',
                      
                 ]

    def parse_threads(self,response):
        self.log("access url:%s"% response.url)
        hxs = HtmlXPathSelector(response)
        all =hxs.select('//tbody[starts-with(normalize-space(@id),"normalthread_")]/tr');
        for thread in all:
            content=thread.select("th");
            relative_link=content.select('a[1]/@href').extract()[0];
            absolute_link= urlparse.urljoin(response.url, relative_link.strip())
            title = content.select('a[1]/text()').extract()[0]
            time=thread.select("td[normalize-space(@class)='by']");
            create_time=time[0].select('em/span/text()').extract()[0] 
            self.log("+++link:%s  time:%s"%(absolute_link,create_time));
            post = {"url":absolute_link,
                    "title":title,
		    "tag": self.name,
		    "classify":self.classify,
		    "grab_at":datetime.datetime.utcnow(),
		    "grab_progress":"0",
                    "create_time":create_time}
	    if createNewThread(post):
                yield Request(absolute_link,callback=self.parse_thread)
        return ;

    def parse_thread(self,response):
        self.log("thread url:%s"% response.url)
        hxs = HtmlXPathSelector(response)
        first_floor= hxs.select('//div[starts-with(normalize-space(@id),"post_")]')[0]
        content=first_floor.select('.//td[starts-with(normalize-space(@id),"postmessage_")]')[0]
        imgs=content.select('.//img/@src').extract();
        if(len(imgs)==0):
	    self.threads_db.remove({"url":response.url})
            return;
	links = content.select('.//a/@href').extract();
        if(len(links)==0):
	    self.threads_db.remove({"url":response.url})
            return;
        #items = [];
        #for img in imgs:
        item = AutobtItem()
	item['name'] = response.url
        item['image_urls'] = imgs 
	item['links']=links
        #inspect_response(response)

	all=content.extract();
	
	ret = parseDetailFromContent(all);

	tt=self.threads_db.find_one({"url":response.url})
	tt["content"]=ret;
	tt['raw_content']=all;
	self.threads_db.save(tt);
	
	if not item['links']:
		return item
        return parse_bt(item);


    def parse(self, response):
	self.log('hi from %s'% response.url);
	return [FormRequest.from_response(response,
                    formdata={'username': 'lupkkkk', 'password': 'DONTlook8240'},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        #inspect_response(response)
        if 'lupkkk' in response.body:
             self.log("login sucessfully")
             for x in self.parse_urls:
                 yield Request(x,callback=self.parse_threads)
             #return Request(self.parse_urls[self.parse_index],
              #                  callback=self.parse_thread);
        else:
             self.log("failed to login")
        return

