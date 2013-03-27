#! /usr/bin/env python

import os
import sys
from drinkz import recipes, db
from drinkz.db import load_db

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

def main(args):
    filename = args[1]

    load_db(filename)

if __name__ == '__main__':
    main(sys.argv)

#db._reset_db()

#db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
#db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

#db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
#db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

#db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
#db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

#db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
#db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'), ('vermouth', '1.5 oz')])
#db.add_recipe(r)

#r2 = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
#db.add_recipe(r2)

#r3 = recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth',
#                                                                          '1.5 oz')])
#db.add_recipe(r3)


fp = open('html/index.html', 'w')
print >>fp, "Hello. Welcome to drinkz. Click a link to navigate."

print >>fp, """
<p>
<a href='recipes.html'>Recipes</a>
<a href='inventory.html'>Inventory</a>
<a href='liquor_types.html'>Liquor Types</a>
"""

fp.close()


fp = open('html/recipes.html', 'w')

print >>fp, """
Recipes:
<table>
  <tr>
    <td>Name:</td>
    <td>Ingredients Needed(ml):</td>
  </tr>
"""
recipe_list = list(db.get_all_recipes())
for r in recipe_list:
    print >>fp, '<tr>'
    strhtml = '<td>'+r.name+'</td>'
    print >>fp, strhtml
    ing = r.need_ingredients()
    if len(ing) == 0:
        strhtml = '<td>HAVE ALL INGREDIENTS</td>'
    else:
        strhtml = '<td>missing: '
        for i in ing:
            strhtml += str(i)
        strhtml += '</td>'
    print >>fp, strhtml
    print >>fp, '</tr>'
print >>fp, """
</table>
<a href='index.html'>Back To Index</a>
"""

fp.close()


fp = open('html/liquor_types.html', 'w')

print >>fp, """
Types of Liquor:
<ul>
"""
for mfg, liquor in db.get_liquor_inventory():
    print >>fp, '<li> '+str(liquor)
print >>fp, """
</ul>
<a href='index.html'>Back To Index</a>
"""

fp.close()


fp = open('html/inventory.html', 'w')

print >>fp, """
Inventory:
<table>
  <tr>
    <td>Liquor:</td>
    <td>Amount(ml):</td>
  </tr>
"""
for mfg, liquor in db.get_liquor_inventory():
    print >>fp, '<tr>'
    print >>fp, '<td>'+str(mfg)+' '+str(liquor)+'</td>'
    print >>fp, '<td>'+str(db.get_liquor_amount(mfg, liquor))+'</td>'
    print >>fp, '</tr>'
print >>fp, """
</table>
<a href='index.html'>Back To Index</a>
"""

fp.close()
