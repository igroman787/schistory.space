#!/usr/bin/env python3
# -*- coding: utf_8 -*-

#from updateDatabase import *


###
### Start of the program
###

#if __name__ == "__main__":
#	Init()
#end if

#olinKl

import socket

sock = socket.socket()
server = ('localhost', 4800)
sock.connect(server)
print("connected")

message = b'<nickname>olinKl</nickname>'
sock.send(message)
print("send:", message)

data = sock.recv(1024)
print("get:", data)
sock.close()
