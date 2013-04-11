#This file was just used for testing
#!/usr/bin/env python
import sys
import socket

s = socket.socket()
host = socket.gethostname()
port = int(sys.argv[1])

print 'connecting...'
s.connect((host, port))
s.send("GET / HTTP/1.0\n\n")
data = s.recv(1024)
while data != "":
    print data
    data = s.recv(1024)
print 'done'
s.close()
