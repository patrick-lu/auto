# Scrapy settings for reply project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'reply'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['reply.spiders']
NEWSPIDER_MODULE = 'reply.spiders'
DEFAULT_ITEM_CLASS = 'reply.items.ReplyItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"

IMAGES_STORE = '../btimgs/'
BTFILES_STORE = '../btfiles/'
DB_NAME = 'autobt'
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 1
