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
    name = 'rarbg'
    classify = 'west'
    db_name=settings['DB_NAME']
    conn = Connection()
    db = Database(conn,db_name)
    threads_db = db.threads

    
    #download_delay =8
    #randomize_download_delay=True;
    #allowed_domains = ['www.google.com']
    start_urls = [
                     'http://www.rarbg.com',
                 ]
    parse_urls = [
		     'http://www.rarbg.com/torrents.php?category=4',
                      
                 ]

    def parse_threads(self,response):
        self.log("access url:%s"% response.url)
        hxs = HtmlXPathSelector(response)
	#inspect_response(response)
	block=hxs.select('//tr[normalize-space(@class)="head"]/../tr[normalize-space(@class)="cbg"]')
	block_num=len(block)
	threads=hxs.select('//tr[normalize-space(@class)="head"]/../tr')

        for thread in threads:
	    cls=thread.select('./@class').extract()
	    if(cls[0]=="cbg"):
		block_num-=1;
		continue
	    if(block_num==0):
		relative_link=thread.select('.//a[1]/@href').extract()
		if relative_link :
			relative_link=relative_link[0]
		else:
			self.log("ERR:%s"%thread.extract());
			continue
		absolute_link= urlparse.urljoin(response.url, relative_link.strip())
		title = thread.select('.//a[1]/text()').extract()[0]
		time=thread.select(".//td[normalize-space(@class)='smalltxt']")[0]
		create_time= time.select('./text()').extract()[1]

		self.log("+++link:%s  time:%s"%(absolute_link,create_time));
                post = {"url":absolute_link,
                    		"title":title,
		    		"tag": self.name,
		    		"grab_at":datetime.datetime.utcnow(),
		    		"grab_progress":"0",
				"classify":self.classify,
                    		"create_time":create_time}
                if createNewThread(post):
                	yield Request(absolute_link,callback=self.parse_thread)
        return ;

    def parse_thread(self,response):
        self.log("thread url:%s"% response.url)
	inspect_response(response)
        hxs = HtmlXPathSelector(response)
        first_floor= hxs.select('//table[normalize-space(@cellpadding)="6"]')[0]
	content=first_floor.select('./tr[1]/td')

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

	all=content.extract()[0];

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
        for x in self.parse_urls:       #beause of no user account
             yield Request(x,callback=self.parse_threads)
	#return [FormRequest.from_response(response,
        #            formdata={'loginuser': 'lupkkkk', 'loginpwd': 'DONTlook8240','hideid':'0','cktime':'86400','jumpurl':'http://aisex.com/bt/index.php'},
        #            callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        #inspect_response(response)
	debug = 0;
        if 'lupkkk' in response.body:
            self.log("login sucessfully")
	    if settings['debug'] or debug:
		self.log("enter debug mode. make sure that this link has been stored in db")
		url = 'http://aisex.com/bt/htm_data/5/1206/530628.html'
		post = {"url":url,
                                "title":"test",
                                "tag": self.name,
                                "grab_at":datetime.datetime.utcnow(),
                                "grab_progress":"0",
                                "classify":self.classify,
                                "create_time":'test'}
                createNewThread(post)
                yield Request(url,callback=self.parse_thread)
		return
            for x in self.parse_urls:
                 yield Request(x,callback=self.parse_threads)
             #return Request(self.parse_urls[self.parse_index],
              #                  callback=self.parse_thread);
        else:
             self.log("failed to login")
        return

