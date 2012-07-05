# Scrapy settings for wbsource project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'wbsource'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['wbsource.spiders']
NEWSPIDER_MODULE = 'wbsource.spiders'
DEFAULT_ITEM_CLASS = 'wbsource.items.WbsourceItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"

ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline',
		  'wbsource.FilePipeline.FilePipeline',
		  'wbsource.DBPipeline.DBPipeline'
			]

DB_NAME = 'weibo'

FILES_STORE = '../wbimgs/'
