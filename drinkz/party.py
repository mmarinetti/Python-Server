import db

class Party(object):
    def __init__(self, user, music="", crash_spots=0, DD=0, rating=0, liquor=[]):
        self.user = user
        self.rating = rating
        self.liquor = liquor
        self.music = music
        self.crash_spots = crash_spots
        self.DD = DD

    def add_liquor(self, l):
        self.liquor.append(l)

    def get_liquors(self):
        for i in self.liquor:
            yield i
