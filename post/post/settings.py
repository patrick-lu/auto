# Scrapy settings for post project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'post'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['post.spiders']
NEWSPIDER_MODULE = 'post.spiders'
DEFAULT_ITEM_CLASS = 'post.items.PostItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

