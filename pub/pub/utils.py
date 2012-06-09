from scrapy.conf import settings
import zmq

from pymongo import Connection
from pymongo.database import Database
host = "127.0.0.1"
def selectToPub():
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://"+host+":6100")
	msg={"cmd":"ask_pub"}
	print ("ask monster for a url")
	socket.send_json(msg);
	url = socket.recv()
	print ("try to publish %s"%url)
	if url == "" :
		return ""
	db_name=settings['DB_NAME']
	conn = Connection()
	db=Database(conn,db_name)
	threads_db = db.threads
	item=threads_db.find_one({"url":url});
	return item;

def saveItem(item):
	db_name=settings['DB_NAME']
	conn = Connection()
	db=Database(conn,db_name)
	threads_db = db.threads
	threads_db.save(item)	
