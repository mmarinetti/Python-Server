from sets import Set
import recipes
import sqlite3, os

"""
Database functionality for drinkz information.
I am using a set to store the recipes because
it would be useless to store multiple definitions
of the same recipe
"""

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = Set()
_inventory_db = {}
_recipes_db = Set()
_parties_db = []

"""
try:
    os.unlink('bottle_types.db')
except OSError:
    pass

db_bt = sqlite3.connect('database.db')
c = db_bt.cursor()
c.execute('CREATE TABLE bottle_types_db (id INTEGER PRIMARY KEY ASC, \
                             m TEXT, l TEXT, t TEXT)')

try:
    os.unlink('inventory.db')
except OSError:
    pass

db_i = sqlite3.connect('inventory.db')
cursor_inventory = db_i.cursor()
cursor_inventory.execute('CREATE TABLE inventory_db (id INTEGER PRIMARY KEY ASC, \
                          m TEXT, l TEXT, a FLOAT)')
"""

c = sqlite3.connect('database.db').cursor()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db, _parties_db
    _bottle_types_db = Set()
    _inventory_db = {}
    _recipes_db = Set()
    _parties_db = []

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))
    #c.execute('INSERT INTO bottle_types_db (m, l, t) VALUES (?, ?, ?)', (mfg, liquor, typ))
    #sqlite3.connect('database.db').commit()
    _inventory_db[(mfg, liquor)] = 0

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    #c.execute('SELECT COUNT(1) FROM bottle_types_db WHERE \
    #           bottle_types_db.m=? AND bottle_types_db.l=?', (mfg, liquor,))
    #if c.fetchone()[0]:
    #    return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    a = _inventory_db.get((mfg, liquor))
    #c.execute('SELECT * FROM bottle_types_db')
    #c.fetchall()
    #c.execute('SELECT * FROM inventory_db WHERE m=? AND l=?', (mfg, liquor,))
    #a = c.fetchone()[2]
    try:
        a += convert_to_ml(amount)
        _inventory_db[(mfg, liquor)] = a
    except ValueError:
        pass

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db.keys():
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    return _inventory_db.get((mfg, liquor))

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db.keys():
        yield m, l

def check_inventory_for_type(type):
    liquors = Set()
    for (m, l, t) in _bottle_types_db:
        if type == t:
            liquors.add((m, l))
    return liquors

def convert_to_ml(amount):
    if amount[-2:] == "ml":
        return float(amount[:-2])
    elif amount[-2:] == "oz":
        return float(amount[:-2])*29.5735
    elif amount[-6:] == "gallon":
        return float(amount[:-6])*3785.41
    elif amount[-5:] == "liter":
        return float(amount[:-5])*1000

def add_recipe(r):
    _recipes_db.add(r)

def get_recipe(name):
    for r in _recipes_db:
        if r.name == name:
            return r

def get_all_recipes():
    for r in _recipes_db:
        yield r

def add_party(p):
    _parties_db.append(p)

def get_all_parties():
    for p in _parties_db:
        yield p
