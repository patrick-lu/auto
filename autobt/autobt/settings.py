# Scrapy settings for autobt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'autobt'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['autobt.spiders']
NEWSPIDER_MODULE = 'autobt.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
#USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"
#ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
ITEM_PIPELINES = ['autobt.imagedown.MyImagePipeline',
		  'autobt.btdown.BTPipeline',
		  'autobt.DBPipeline.DBPipeline'
			]
IMAGES_STORE = '../btimgs/'
BTFILES_STORE = '../btfiles/'
