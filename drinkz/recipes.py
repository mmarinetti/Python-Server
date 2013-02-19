import db

class Recipe(object):
    def __init__(self, name, ingr):
        self.name = name
        self.ingredients = ingr

    def need_ingredients(self):
        need = []
        amount = 0
        for i in self.ingredients:
            typehave = db.check_inventory_for_type(i[0])
            most = 0
            for (m, l) in typehave:
                if db.get_liquor_amount(m, l) > most:
                    amount = db.get_liquor_amount(m, l)
                    most = amount

            amount = db.convert_to_ml(i[1])-amount
            if amount > 0:
                need.append((i[0], amount))

        return need
