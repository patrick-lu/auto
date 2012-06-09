from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from pymongo import Connection
from pymongo.database import Database
from scrapy.shell import inspect_response
import urlparse

import re


def get_reply():
	msgs=[
		u'\u8c22\u8c22\u697c\u4e3b\u5206\u4eab\uff01\uff01',
	     ]
	reply = msgs[0]
	return reply	


