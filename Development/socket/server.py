#!/usr/bin/env python

# Echo server program
import socket

HOST = ''                # Symbolic name meaning the local host
PORT = 50111              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

while 1:
    data = conn.recv(1024)
    print data
    if not data: break
    conn.send("thank you")
conn.close()