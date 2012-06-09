from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.shell import inspect_response
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.conf import settings
from pymongo import Connection
from scrapy.conf import settings
from pymongo.database import Database
import urlparse
import datetime

from time import sleep
from reply.utils import get_reply
import zmq

class AisexSpider(BaseSpider):
    name = 'aisex'
    db_name=settings['DB_NAME']
    conn = Connection()
    db = Database(conn,db_name)
    threads_db = db.threads

    limit=50;
    lan="GBK"

    user_name="lupkkkk"
    user_pass="DONTlook8240"
 
    context = zmq.Context()
    manager = context.socket(zmq.REQ)
    manager.connect("tcp://127.0.0.1:6301")
    
    download_delay =110
    randomize_download_delay=False;
    CONCURRENT_REQUESTS = 1
    #allowed_domains = ['www.google.com']
    start_urls = [
                     'http://aisex.com/bt/login.php',
		     #'http://108.170.27.83/forum-2-1.html',
		     #'http://108.170.27.83/forum-2-2.html',
                 ]
    def creat_msg(cmd):
	msg={};
	msg['cmd']=cmd;
	msg['tag']=self.name;
	return msg

    def echo(msg):
	manager.send_json(msg)
	return manager.recv()

    def goto_thread(self,response):
        self.log("goto url:%s"% response.url)
	#inspect_response(response)
	reply=get_reply();
        #inspect_response(response)
	#self.log(reply);
        #inspect_response(response)
	reply=reply.encode(self.lan)
	#req = FormRequest.from_response(response,
#		formdata={'atc_content':reply},
#		callback=self.reply_thread
#		)
	#req.meta['url']=response.url;
	#return [req]
	return [FormRequest.from_response(response,
			formdata={'atc_content':reply},
			callback=self.reply_thread,dont_filter=True)]

    def reply_thread(self, response):
	#url = response.meta["url"]
	#self.log(url)
	self.log(response.url)
	url = response.url
	if(url.find('post.php')> -1):
		self.log('reply ERROR')
		self.log(response.body.decode('GBK'))
	else:
		self.log('reply successfully')
		#inspect_response(response)
		thread = self.threads_db.find_one({'url':url})
		thread['reply'][self.user_name]="today"
		self.threads_db.save(thread)
	return self.find_new_thread(response)

    def parse(self, response):
	self.log('prepare reply from %s'% response.url);
	count = self.threads_db.find({'reply.'+self.user_name:{'$exists':False},'tag':self.name}).count()
	self.log('%d threads are available'%count)
	if(count==0):
		return

	msg=self.create_msg("max")
	self.limit=self.echo(msg)
	self.log('max to reply %d threads'%self.limit)

	#sleep(10)
	return [FormRequest.from_response(response,
                    formdata={'loginuser': self.user_name, 'loginpwd': self.user_pass,'hideid':'0','cktime':'86400','jumpurl':'http://aisex.com/bt/index.php'},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        #inspect_response(response)
        if self.user_name in response.body:
             self.log("login sucessfully")
	     return self.find_new_thread(response);
        else:
             self.log("failed to login")
        return

    def find_new_thread(self,response):
	self.log("try to find a thread")
	if self.limit ==0:
		return 
	self.limit =self.limit -1;
	# add a url check in case of endless loop
	thread = self.threads_db.find_one({'reply.'+self.user_name:{'$exists':False},'tag':self.name})
	if thread :
		#thread['reply'][self.user_name]="today"
		#self.threads_db.save(thread)
		self.log("found %s"%thread['url'])
		return Request(thread['url'],callback=self.goto_thread)
	else:
		self.log("no new thread to reply");
		return
