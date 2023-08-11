from colorama import Style


class Tile:
    # tile serves as basic possibility for cell state
    def __init__(self, index, char, colour, weight, walkable):
        self.index = index
        self.char = char
        self.colour = colour
        self.weight = weight  # ±1 to alter frequency of random selection
        self.walkable = walkable

        # valid tile placements corresponding to directions
        self.valid_adjacents = []

    def set_rules(self, edge_rules):
        specific_rules = list(filter(lambda x: x[0].index == self.index, edge_rules))
        [self.valid_adjacents.append(rule[1]) for rule in specific_rules]

    def __str__(self):
        return f"{self.colour}{self.char}{Style.RESET_ALL}"
