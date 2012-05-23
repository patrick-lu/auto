from scrapy.exceptions import DropItem
from autobt.items import AutobtItem
from pymongo import Connection

class DBPipeline(object):
	def __init__(self):
		self.conn = Connection()
		self.db = self.conn.autobt
		self.threads_db = self.db.threads
	
	def process_item(self, item,spider):
		tt=self.threads_db.find_one({"url":item["name"]});
		for key in item:
			tt[key]=item[key]

		self.threads_db.save(tt)

		return item;
