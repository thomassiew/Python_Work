import zmq
import random
import sys
import time

port = "5557"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

print "Talk"
name = raw_input()
while True:

    msg = socket.recv()
    print msg
    if name is None:
        socket.send('...')
    else:
        socket.send(name)
    time.sleep(.5)