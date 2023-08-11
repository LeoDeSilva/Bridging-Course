from items.item import *


class Key(Item):
    def __init__(self):
        super().__init__(KEY)
        self.consumable = True


class Berry(Item):
    def __init__(self):
        super().__init__(BERRY)
        self.consumable = True
