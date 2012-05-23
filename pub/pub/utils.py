from scrapy.conf import settings

from pymongo import Connection
from pymongo.database import Database

def selectToPub():
	db_name=settings['DB_NAME']
	conn = Connection()
	db=Database(conn,db_name)
	threads_db = db.threads
	item=threads_db.find_one();
	return item;

def saveItem(item):
	db_name=settings['DB_NAME']
	conn = Connection()
	db=Database(conn,db_name)
	threads_db = db.threads
	threads_db.save(item)	
