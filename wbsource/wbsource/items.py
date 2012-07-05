# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WbsourceItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url = Field()
    file_urls = Field()
    files = Field()
    content = Field()
    grab_time = Field()
