# Scrapy settings for pub project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pub'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pub.spiders']
NEWSPIDER_MODULE = 'pub.spiders'
DEFAULT_ITEM_CLASS = 'pub.items.PubItem'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"

IMAGES_STORE = '../btimgs/'
BTFILES_STORE = '../btfiles/'
DB_NAME = 'autobt'

adfly_name='lup2k@126.com'
adfly_pass='DONTlook8240'

linkbucks_name='lup2k'
linkbucks_pass='moneyM@n1y'

imageporter_name='lupkkk'
imageporter_pass='DONTlook8240'

shareimage_name='lupkkk'
shareimage_pass='DONTlook8240'

imgchili_name='lupkkk'
imgchili_pass='DONTlook8240'
