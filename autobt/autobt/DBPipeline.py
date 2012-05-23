from scrapy.exceptions import DropItem
from autobt.items import AutobtItem
from pymongo import Connection
from pymongo.database import Database
from scrapy.conf import settings

class DBPipeline(object):
	def __init__(self):
		db_name=settings['DB_NAME']
		self.conn = Connection()
		self.db = Database(self.conn,db_name)
		self.threads_db = self.db.threads
	
	def process_item(self, item,spider):
		tt=self.threads_db.find_one({"url":item["name"]});
		for key in item:
			tt[key]=item[key]

		tt["grab_progress"]="1"
		self.threads_db.save(tt)

		return item;
