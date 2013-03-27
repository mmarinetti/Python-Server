#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import recipes, db
import sys

dispatch = {
    '/' : 'index',
    '/recipes' : 'recipes',
    '/error' : 'error',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_types',
    '/convert_to_ml' : 'convert_to_ml',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """\
<html>
<head>
<title>Drinkz</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<script>
function popUpBox()
{
alert("Welcome to Drinkz!");
}
</script>
<body>
<h1>Hello! Welcome to drinkz. Click a link to navigate.</h1>
<p>
<a href='recipes'>Recipes</a>,
<a href='inventory'>Inventory</a>,
<a href='liquor_types'>Liquor Types</a>,
<a href='convert_to_ml'>Convert to ml</a>
<p>
<input type="button" onclick="popUpBox()" value="Show alert box" />
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."

        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = """\
<html>
<head>
<title>Recipes</title>
<style type='text/css'>
h1 {color:red;}
hody {
font-size: 14px;
}
</style>
</head>
<body>
<h1>Recipes:</h1>
<table>
  <tr>
    <td>Name:</td>
    <td>Ingredients Needed(ml):</td>
  </tr>
"""
        recipe_list = list(db.get_all_recipes())
        for r in recipe_list:
           data += '<tr>'
           strhtml = '<td>'+r.name+'</td>'
           data += strhtml
           ing = r.need_ingredients()
           if len(ing) == 0:
               strhtml = '<td>HAVE ALL INGREDIENTS</td>'
           else:
               strhtml = '<td>missing: '
               for i in ing:
                   strhtml += str(i)
               strhtml += '</td>'
           data += strhtml
           data += '</tr>'
        data += """\
</table>
<a href='./'>Back To Index</a>
</body>
</html>
"""

        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = """\
<html>
<head>
<title>Inventory</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
</head>
<body>
<h1>Inventory:</h1>
<table>
  <tr>
    <td>Liquor:</td>
    <td>Amount(ml):</td>
  </tr>
"""
        for mfg, liquor in db.get_liquor_inventory():
            data += '<tr>'
            data += '<td>'+str(mfg)+' '+str(liquor)+'</td>'
            data += '<td>'+str(db.get_liquor_amount(mfg, liquor))+'</td>'
            data += '</tr>'
        data += """\
</table>
<a href='./'>Back To Index</a>
</body>
</html>
"""
       
        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_types(self, environ, start_response):
        content_type = 'text/html'
        data = """\
<html>
<head>
<title>Liquor Types</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
</head>
<body>
<h1>Types of Liquor:</h1>
<ul>
"""
        for mfg, liquor in db.get_liquor_inventory():
            data += '<li> '+str(liquor)
        data += """\
</ul>
<a href='./'>Back To Index</a>
</body>
<html>
"""

        start_response('200 OK', list(html_headers))
        return [data]

    def convert_to_ml(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['amount'][0]
        units = results['units'][0]

        content_type = 'text/html'
        ml = db.convert_to_ml(amount+units)
        data = """\
<html>
<head>
<title>Converted to ml</title>
<style type='text/css'>
h1 {color:red}
body {
font-size: 14px;
}
</style>
</head>
<body>
<h1>Converted</h1>
"""
        data += "Amount: %s %s to ml: %s" % (amount, units, ml)
        data += """
<p>
<a href='./'>return to index</a>
</body>
</html>
"""

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

    def rpc_convert_units_to_ml(self, amount):
         return db.convert_to_ml(amount)

    def rpc_get_recipe_names():
        for r in db.get_all_recipes():
            yield r.name

    def rpc_get_liquor_inventory():
        inventory = []
        for l in db.get_liquor_inventory():
            inventory.append(l)
        return inventory
    
def form():
    return """
<html>
<head>
<title>Convert to ml</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
</head>
<body>
<h1>Convert to ml</h1>
</body>
</html>
<form action='recv'>
Amount: <input type='text' name='amount' size'20'>
Units: <input type='text' name='units' size='20'>
<input type='submit'>
</form>
"""

def main(args):
    filename = args[1]
    load_db(filename)

if __name__ == '__main__':
    main(sys.argv)

    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
