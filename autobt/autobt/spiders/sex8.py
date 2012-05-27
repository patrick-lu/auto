from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from autobt.items import AutobtItem
from scrapy.shell import inspect_response
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.conf import settings
from autobt.items import AutobtItem
from pymongo import Connection
from pymongo.database import Database
import urlparse
import datetime


from time import sleep

class Sex8Spider(CrawlSpider):
    name = 'sex8'
    db_name=settings['DB_NAME']
    conn = Connection()
    db = Database(conn,db_name)
    threads_db = db.threads

    
    #download_delay =10
    #randomize_download_delay=True;
    #allowed_domains = ['www.google.com']
    start_urls = [
                     'http://x8zz.com/index.php',
		     #'http://108.170.27.83/forum-2-1.html',
		     #'http://108.170.27.83/forum-2-2.html',
                 ]
    parse_urls = [
		     'http://x8zz.com/thread-htm-fid-96.html',
		    # 'http://108.170.27.83/forum-2-2.html',
                      
                 ]

    def parse_threads(self,response):
        self.log("access url:%s"% response.url)
        hxs = HtmlXPathSelector(response)
	#inspect_response(response)
        all =hxs.select("//div[normalize-space(@class)='main-wrap']/div/div/table/tbody[1]/tr");
	thread_start=0;
	i=0
        for thread in all:
	    i=i+1
	    if(thread_start==0 and thread.select('td[normalize-space(@colspan)="6"]')):
	    	thread_start=1;
	    elif(thread_start==1 and not thread.select('td[normalize-space(@colspan)="6"]')):
		title=""
		tmp=thread.select('td[2]/a[normalize-space(@class)="subject"]//font/text()');
		if tmp:
			title=tmp.extract()[0];
		else:
			tmp=thread.select('td[2]/a[normalize-space(@class)="subject"]/text()');
			if tmp:
				title=tmp.extract()[0];
			else:

				self.log("ERROR===>%s"% thread.extract())
				continue
            	relative_link=thread.select('td[2]/a[normalize-space(@class)="subject"]/@href').extract()[0];
            	absolute_link= urlparse.urljoin(response.url, relative_link.strip())
            	create_time=thread.select('td[3]/div/text()').extract()[0]
            	self.log("+++link:%s  time:%s"%(absolute_link,create_time));
	    	post = self.threads_db.find_one({"url":absolute_link})
            	if( not post):
                	post = {"url":absolute_link,
                   		"title":title,
		    		"tag": self.name,
		    		"grab_at":datetime.datetime.utcnow(),
		    		"grab_progress":"0",
                    		"create_time":create_time}
                	self.threads_db.insert(post)
                	yield Request(absolute_link,callback=self.parse_thread)
        return ;

    def parse_thread(self,response):
        self.log("thread url:%s"% response.url)
        hxs = HtmlXPathSelector(response)
	#inspect_response(response)

	content=hxs.select("//div[normalize-space(@id)='read_tpc'][1]");
        imgs=content.select('.//img/@src').extract();
	for img in imgs:
		if img.find("http")!=0:
			imgs.remove(img);
        if(len(imgs)==0):
	    self.threads_db.remove({"url":response.url})
            return;
        #items = [];
        #for img in imgs:
        item = AutobtItem()
	item['name'] = response.url
        item['image_urls'] = imgs 
        #inspect_response(response)

	all=content.extract()[0];
	con={"name":"","size":"","format":"","time":""}
	colon =  u'\uff1a' 
	tags={
         u'\u5f71\u7247\u540d\u7a31':"name",
         u'\u5f71\u7247\u540d\u79f0':"name",
         u'\u5f71\u7247\u683c\u5f0f':"format",
         u'\u5f71\u7247\u5927\u5c0f':"size",
         u'\u5f71\u7247\u957f\u5ea6':"time",
         u'\u5f71\u7247\u65f6\u95f4':"time",
        }

	for key in tags:
		index =all.find(key);
		if(index >0):
			name =all[index:]
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
						con[tags[key]] = name[(index+1):]

	tt=self.threads_db.find_one({"url":response.url})
	tt["content"]=con;
	tt['raw_content']=all;
	if con['name']=="":
		self.threads_db.remove({"url":response.url})
		return;
	self.threads_db.save(tt);
        return item;

    def parse(self, response):
	self.log('hi from %s'% response.url);
	return [FormRequest.from_response(response,
                    formdata={'pwuser': 'lupkkkk', 'pwpwd': 'DONTlook8240'},
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

