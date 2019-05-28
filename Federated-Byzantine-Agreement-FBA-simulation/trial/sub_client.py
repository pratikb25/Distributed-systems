
import sys
import zmq
import time

port = "5556"

#socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:%s" % port)

topicfilter = ''
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

while True:
	string = socket.recv()
	print("Received [%s]" % string);
	time.sleep(1)

