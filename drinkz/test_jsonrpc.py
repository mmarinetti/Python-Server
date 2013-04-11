import simplejson
import app
import db
import recipes
import StringIO

def call_remote(method, params, id):
    stuff = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(stuff)

    file = StringIO.StringIO()
    file.write(encoded)
    file.seek(0)

    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['wsgi.input'] = file
    environ['CONTENT_LENGTH'] = len(encoded)

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    response = app_obj(environ, my_start_response)

    results = simplejson.loads(response[0])

    assert d['status'] == '200 OK'
    assert ('Content-Type', 'application/json') in d['headers']

    return results

def test_json_convert_to_ml():
    results = call_remote(method='convert_units_to_ml', params=['20 oz'], id=1)

    assert results['result'] == 591.47, results['result']

def test_json_recipe_names():
    db._reset_db()

    r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    db.add_recipe(r)

    results = call_remote(method='get_recipe_names', params=[], id=1)

    assert 'scotch on the rocks' in results['result'], results['result']

def test_json_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    results = call_remote(method='get_liquor_inventory', params=[], id=1)

    assert ['Johnnie Walker', 'black label'] in results['result'], results['result']

def test_json_add_recipe():
    db._reset_db()
    
    call_remote(method='add_recipe', params=['scotch on the rocks', 
                                             'blended scotch', '4 oz'], id=1)

    assert db.get_recipe('scotch on the rocks').name == 'scotch on the rocks'

def test_json_add_liquor_type():
    db._reset_db()

    call_remote(method='add_liquor_type', params=['Johnnie Walker', 'black label',
                                                  'blended scotch'], id=1)

    assert db._check_bottle_type_exists('Johnnie Walker', 'black label')

def test_json_add_to_inventory():
    db._reset_db()

    call_remote(method='add_liquor_type', params=['Johnnie Walker', 'black label',
                                                  'blended scotch'], id=1)
    call_remote(method='add_to_inventory', params=['Johnnie Walker', 'black label',
                                                   '4 oz'], id=1)

    assert db.get_liquor_amount('Johnnie Walker', 'black label') == 118.294
