"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "Johnnie Walker,Black Label,100 oz"
    fp = StringIO(data)
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 2957.35, amount

def test_get_liquor_amount_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "Johnnie Walker,Black Label,1000 ml"
    data2 = "Johnnie Walker,Black Label,100 oz"
    fp = StringIO(data)
    fp2 = StringIO(data2)
    n = load_bulk_data.load_inventory(fp)
    n2 = load_bulk_data.load_inventory(fp2)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 3957.35, amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_recipes_1():
    db._reset_db()

    data = "scotch on the rocks,blended scotch,4 oz,adfs, 8 oz"
    fp = StringIO(data)
    n = load_bulk_data.load_recipes(fp)

    assert db.get_recipe('scotch on the rocks').name == 'scotch on the rocks'
    assert n == 1, n

def test_bulk_load_recipes_2():
    db._reset_db()

    data = "scotch on the rocks,blended scotch, 4 oz"
    fp = StringIO(data)
    n = load_bulk_data.load_recipes(fp)

    assert db.get_recipe('scotch on the rocks').name == 'scotch on the rocks'
    assert n == 1, n

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_1():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt',
'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_recipes_1():
    scriptpath = 'bin/load-recipes'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/recipes-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x

def test_skip_comments():
    db._reset_db()

    data = "#Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n

def test_skip_blank():
    db._reset_db()

    data = " "
    fp = StringIO(data)
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n

def test_convert_ml():
    x = db.convert_to_ml("10 ml")

    assert x == 10, x

def test_convert_oz():
    x = db.convert_to_ml("20 oz")

    assert x == 591.47, x

def test_convert_gallon():
    x = db.convert_to_ml("2 gallon")

    assert x == 7570.82, x

def test_convert_liter():
    x = db.convert_to_ml("3 liter")

    assert x == 3000, x
