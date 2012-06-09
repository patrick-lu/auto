#!/usr/bin/env python
import zmq

host="127.0.0.1:6000"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://"+host)

#for i in range(10):
msg = {'cmd':'start_reply'}
msg = {'cmd':'start_work'}
	#msg = json.dumps(msg)
socket.send_json(msg)
msg_in = socket.recv();
