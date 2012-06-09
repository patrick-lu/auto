#!/usr/bin/env python
import zmq
import json
from random import choice
from time import time
import datetime
from pymongo import Connection

class info:
	alive=0
	running=0
	
	def __init__(self, alive):
		self.start = int(time())
		self.end = int(time())
		self.alive=alive
	def start_date():
		return datetime.datetime.fromtimestamp(int(self.start)).strftime('%Y-%m-%d %H:%M:%S')
	def end_date():
		return datetime.datetime.fromtimestamp(int(self.end)).strftime('%Y-%m-%d %H:%M:%S')
		

tags = ['aisex','xiaav']
tag = choice(tags)

conn = Connection()
db = conn.autobt
threads_db = db.threads

host='127.0.0.1'
context = zmq.Context()
autobt_srv = context.socket(zmq.REP)
autobt_srv.bind("tcp://"+host+":6000")

reply_srv = context.socket(zmq.REP)
reply_srv.bind("tcp://"+host+":6300")

pub_srv = context.socket(zmq.REP)
pub_srv.bind("tcp://"+host+":6100")

post_srv = context.socket(zmq.REP)
post_srv.bind("tcp://"+host+":6200")

bc = context.socket(zmq.PUB)
bc.bind("tcp://"+host+":6666")

poll = zmq.Poller()
poll.register(autobt_srv, zmq.POLLIN)
poll.register(reply_srv, zmq.POLLIN)
poll.register(pub_srv, zmq.POLLIN)
poll.register(post_srv, zmq.POLLIN)

status={};
srv_status={};
'''
 status['tag']['autobt']['running']
 status['tag']['autobt']['running']
 status['tag']['autobt']['start']
 status['tag']['autobt']['end']
 status['tag']['autobt']['interval']
 status['tag']['autobt']['pri']=0
'''
def main():
	print "main"

def autobt_handler(m):
	msg=json.loads(m)
	if msg['cmd'] == 'start_work':
		srv_status['autobt']=1
	print msg
	return "";

def pub_handler(m):
	msg=json.loads(m)
	print msg
	ret=""
	if msg['cmd'] == 'start_work':
		srv_status['pub']=1
	elif msg['cmd']=='ask_pub':
		#todo: select one based on records in database
		#tag=choice(tags)
		tag='aisex'
		item=threads_db.find_one({'grab_progress':'1','images':{'$exists':True},'btfile':{'$exists':True},'publish':{'$exists':False},'tag':tag})
		if item:
			print ("publish %s"% item['url'])
			ret=item['url']
		else:
			print "no item to publish, need to grab!!"		

		

	return ret;


def post_handler(m):
	msg=json.loads(m)
	print msg
	ret=""
	if msg['cmd'] == 'start_work':
		srv_status['poster']=1
	elif msg['cmd']=='ask_post':
		#todo: select one based on records in database
		#tag=choice(tags)
		tag='aisex'
		item=threads_db.find_one({'pub_progress':'1','post_progress':{'$exists':False},'tag':tag})
		if item:
			ret=item['url']
		else:
			print "no item to post for %s, need to pub!!"%tag		
	
while True:
	sockets = dict(poll.poll(10000))

	if autobt_srv in sockets:
		if sockets[autobt_srv] == zmq.POLLIN:
			msg = autobt_srv.recv()
			ret=autobt_handler(msg)
			autobt_srv.send(ret)
			msg = "autobt "+msg
			bc.send(msg)
	if reply_srv in sockets:
		if sockets[reply_srv] == zmq.POLLIN:
			msg = reply_srv.recv()
			print "MSG:",msg
			reply_srv.send(msg)
			msg = "reply "+msg
			bc.send(msg)
	if pub_srv in sockets:
		if sockets[pub_srv] == zmq.POLLIN:
			msg = pub_srv.recv()
			ret=pub_handler(msg)
			pub_srv.send_unicode(ret)
			msg = "pub "+msg
			bc.send(msg)

	if post_srv in sockets:
		if sockets[post_srv] == zmq.POLLIN:
			msg = post_srv.recv()
			ret=post_handler(msg)
			post_srv.send_unicode(ret)
			msg = "post "+msg
			bc.send(msg)
	if reply_srv in sockets:
		if sockets[reply_srv] == zmq.POLLIN:
			msg = reply_srv.recv()
			print "MSG:",msg
			reply_srv.send(msg)
			msg = "reply "+msg
			bc.send(msg)
	main();
