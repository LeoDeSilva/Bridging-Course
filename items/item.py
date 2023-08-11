MAP = "map"
COMPASS = "compass"
KEY = "key"
BERRY = "berry"


class Item:
    def __init__(self, item):
        self.item = item
        self.consumable = False
    
    def use(self, world):
        pass
