import random
import socket
import time
from app import SimpleApp
import StringIO

s = socket.socket()
host = socket.gethostname()
port = random.randint(8000,9999)
s.bind((host, port))

print 'Starting server on', host, port

d = {}
def my_start_response(s, h, return_id=d):
    d['status'] = s
    d['headers'] = h

app_obj = SimpleApp()

s.listen(5)
while True:
    c, addr = s.accept()
    print 'Got connection from', addr

    buffer = c.recv(1024)

    while "\r\n\r\n" not in buffer:
        data = c.recv(1024)
        if not data:
            break
        buffer += data
        print (buffer,)
        time.sleep(1)

    print 'got entire request:', (buffer,)

    lines = buffer.splitlines()
    request_line = lines[0]
    c.send(lines[-1:][0])
    request_type, path, protocol = request_line.split()
    print 'GOT', request_type, path, protocol

    if request_type == "GET":
        if '?' in path:
            path, query_string = path.split('?', 1)

        environ = {}
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query_string

    elif request_type == "POST":
        html = StringIO.StringIO()
        environ = {}
        environ['PATH_INFO'] = path
        environ['REQUEST_METHOD'] = request_type
        environ['CONTENT_LENGTH'] = 0
        environ['wsgi.input'] = html 

    results = app_obj(environ, my_start_response)

    response_headers = []
    for k, v in d['headers']:
        h = "%s: %s" % (k, v)
        response_headers.append(h)

    response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)

    c.send("HTTP/1.0 %s\r\n" % d['status'])
    c.send(response)
    c.close()

