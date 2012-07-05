from scrapy.spider import BaseSpider
from scrapy.shell import inspect_response
from scrapy.selector import HtmlXPathSelector
from wbsource.items import WbsourceItem

class RedditSpider(BaseSpider):
    name = "reddit"
    #allowed_domains = ["www.reddit.com"]
    start_urls = (
        'http://www.reddit.com/r/funny/',
        )

    def parse(self, response):
	self.log("thread url:%s"% response.url)
	#inspect_response(response)
	hxs = HtmlXPathSelector(response)
	content=hxs.select('//div[normalize-space(@class)="content"]')
	items=content.select('//a[contains(@class,"title")]')
	for ii in items:
		#self.log(ii.select('./@href').extract()[0])
		#self.log(ii.select('./text()').extract()[0])
		item = WbsourceItem()
		item['url']=ii.select('./@href').extract()[0]	
		if ii.select('./@rel'):
			continue;
		tmp=ii.select('./@href').extract()
		imgs=[];
		for img in tmp:
		    if img.find(".jpg")>0 or img.find(".png")>0 or img.find(".gif")>0:
			imgs.append(img)
		
		if len(imgs) > 0:
			item['file_urls']=imgs

		item['content']=ii.select('./text()').extract()[0]	
		yield item
