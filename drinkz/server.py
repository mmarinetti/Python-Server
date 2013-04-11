import random
import socket
import time
from app import SimpleApp

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

    data = c.recv(1024)
    if data[:3] == "GET":
        c.send("HTTP/1.0 200 OK")
        environ = {}
        if '/recipes' in data[4:]:
            environ['PATH_INFO'] = '/recipes'
        elif '/inventory' in data[4:]:
            environ['PATH_INFO'] = '/inventory'
        elif '/liquor_types' in data[4:]:
            environ['PATH_INFO'] = '/liquor_types'
        elif '/convert_to_ml' in data[4:]:
            environ['PATH_INFO'] = '/convert_to_ml'
        elif '/add_recipe' in data[4:]:
            environ['PATH_INFO'] = '/add_recipe'
        elif '/add_liquor_type' in data[4:]:
            environ['PATH_INFO'] = '/add_liquor_type'
        elif '/add_to_inventory' in data[4:]:
            environ['PATH_INFO'] = '/add_to_inventory'
        elif '/' in data[5:]:
            environ['PATH_INFO'] = '/'
        else:
            environ['PATH_INFO'] = '/error'
        html = app_obj(environ, my_start_response)
        c.send(html[0])
    else:
        c.send("Wrong Format.")
        c.send("GET /[destination]")

    c.close()
