from scrapy.exceptions import DropItem
from wbsource.items import WbsourceItem
from pymongo import Connection
from pymongo.database import Database
from scrapy.conf import settings
import datetime

class DBPipeline(object):
	def __init__(self):
		db_name=settings['DB_NAME']
		self.conn = Connection()
		self.db = Database(self.conn,db_name)
		self.threads_db = self.db.threads
	
	def process_item(self, item,spider):
		tt=self.threads_db.find_one({"url":item["url"]});
		if not tt:
			item["grab_time"]=datetime.datetime.utcnow()
			obj = {};
			for key in item:
				obj[key]=item[key]
			print(obj)
			self.threads_db.save(obj);

		return item;
