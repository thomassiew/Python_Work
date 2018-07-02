import zmq

import random
import sys
import time

port = "5556"
port2 =  "5557"
context = zmq.Context()
context2 = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)
socket2 = context2.socket(zmq.PAIR)
socket2.bind("tcp://*:%s" % port2)

socket.send("")
socket2.send("")
while True:



    msg = socket.recv()
    socket2.send(msg)
    msg2 = socket2.recv()
    socket.send(msg2)
