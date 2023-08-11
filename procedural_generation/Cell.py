import random
from colorama import Fore, Style


class Cell:
    def __init__(self, x, y, options):
        self.x = x
        self.y = y
        self.options = options
        self.collapsed = False

        self.path = False
        self.bf_searched = False

    def collapse(self):  # weighted random selection from probability space
        # store relative weights of tiles in order in a list 
        weights = [self.options[i].weight for i in range(len(self.options))]
        self.options = [random.choices(self.options, weights=weights, k=1)[0]]
        self.update()

    def update(self):
        self.collapsed = bool(len(self.options) == 1)

    def entropy(self):
        return len(self.options)

    def __str__(self):
        if self.path: 
            return f"{Fore.LIGHTWHITE_EX}{self.options[0].char}{Style.RESET_ALL}"
        return self.options[0].__str__() if len(self.options) == 1 else "?"
