#!/usr/bin/env python
import zmq
from time import sleep
import json
from threading import Thread
import subprocess 
def notify(msg):
	socket.send_json(msg);
	msg_in = socket.recv();

def getMsg():
#	msg=system.recv_json();
	string = system.recv()
	ch,msg = string.split(' ',1);
	msg=json.loads(msg);
	msg['ch']=ch
	print msg
	return msg

host="127.0.0.1"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://"+host+":6100")

system=context.socket(zmq.SUB)
system.connect("tcp://"+host+":6666")

system.setsockopt(zmq.SUBSCRIBE, "system")
system.setsockopt(zmq.SUBSCRIBE, "autobt")

srv = context.socket(zmq.REP)
srv.bind("tcp://"+host+":6101")

poll = zmq.Poller()
poll.register(srv, zmq.POLLIN)
poll.register(system, zmq.POLLIN)


status = {'running':0};
def start():
	status['running'] = 1
	print "start pub"
	log = open('./log',"w")
	app = subprocess.Popen(args='scrapy crawl 400kb', shell=True, stdout=subprocess.PIPE)
	app.wait()
	log.write(app.stdout.read())
	status['running'] = 0
	print "finish pub";
	msg={"cmd":"finish_pub"}
	notify(msg)
	log.close();

def system_handler(msg):
	cmd = msg['cmd']
	print "cmd:"+cmd;
	if(msg['cmd']=="ping"):
		notify({"cmd":"pong"})
	elif cmd == "start_pub":
		if status['running']==0:
			t=Thread(target=start)
			t.start()
		else:
			print "has started "+tag
	else:
		print "unknown cmd"
	return
def worker_handler(msg):
	if(msg['cmd']=="max"):
		srv.send(status[msg['tag']]['max'])
#	elif msg['cmd']=='terminate':
#		srv.send(status[msg['tag']]['terminate'])
		


while True:
	sockets = dict(poll.poll())
	if system in sockets:
		if sockets[system] == zmq.POLLIN:
			msg=getMsg();
			system_handler(msg)
	if srv in sockets:
		if sockets[srv] == zmq.POLLIN:
			msg = srv.recv_json()
			worker_handler(msg)

