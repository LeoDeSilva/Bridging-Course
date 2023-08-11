from colorama import Fore, Style
import random
import os

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.action_count = 1
        self.base_action_count = 1
        self.unit = ""

        self.turn = False
        self.hidden = False
        self.defend = False

    def move(self, board, direction): # abstraction of move, handles valid squares, occupied etc
        position = board.compile((self.x, self.y), direction)
        potential_unit = board.get_unit(position[0], position[1])
        if board.is_valid_location(position) and (potential_unit == None or potential_unit.hidden):
            self.x, self.y = position[0], position[1]
            return True
        return False

    def take_damage(self, unit): # handles attack msg, health and defending 
        self.health = max(self.health-(unit.damage if not self.defend else 0), 0)
        if self.defend:
            self.defend = False
            return f"{self.unit} ({self.x+1},{self.y+1}) defended, no damage was taken"

        return f"{self.unit} ({self.x+1},{self.y+1}) taken damage ({unit.damage}) from {unit.unit} at ({unit.x+1},{unit.y+1}), health: {self.health}"

    def __str__(self):
        if self.turn: 
            return f"{Style.BRIGHT}" + self.repr + f"{Style.RESET_ALL}"
        return self.repr

class PartyUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.player = True

class EnemyUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.target = None
        self.player = False

    def collect_units(self, board):
        adjacents = {}
        for i in range(board.size): adjacents[i] = []

        for unit in board.playerUnits:
            if unit.health <= 0: continue
            band = max(abs(unit.x-self.x), abs(unit.y-self.y))
            adjacents[band].append(unit)

        return adjacents

    # create a path using breadth first search from one tile to another
    def create_path(self, board, target): # start & finish store tile incidies of target tiles
        parents = {}
        queue = [(self.x, self.y)]
        searched = [(self.x, self.y)]

        while queue:
            current_cell = queue.pop(0)

            if current_cell == (target.x, target.y):
                break

            neighbours = [(current_cell[0]-1, current_cell[1]), 
                            (current_cell[0]+1, current_cell[1]), 
                            (current_cell[0], current_cell[1]-1), 
                            (current_cell[0], current_cell[1]+1)
                        ]
        
            for neighbour in neighbours:
                neighbour_cell = board.get_cell(neighbour[0],neighbour[1])

                # ensure neighbour square is not occupied (unless occupied by the target unit)
                unit = board.get_unit(neighbour[0], neighbour[1])
                unit_blocked = unit != None and not (unit.x == target.x and unit.y == target.y)

                # if cell exists and not already searched and not blocked by unit or wall
                if neighbour_cell != None and not (neighbour in searched) and not unit_blocked and neighbour_cell == 0:
                    searched.append(neighbour)
                    queue.append(neighbour)
                    parents[neighbour] = current_cell

        if current_cell[0] != target.x and current_cell[1] != target.y: return [] # path not generated

        path = []
        current_cell = (target.x, target.y)

        # traverse parents dictionary to find root node (ensures shortest path for full route calculated)
        while current_cell != (self.x, self.y):
            path.append(current_cell)
            current_cell = parents[current_cell]

        path.reverse()

        return path

    def handle_ai(self, board):
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        ai_update = ""

        if self.health == 0: return ai_update # no action if dead

        # collect all players immediately surrounding enemy unit
        adjacents = self.collect_units(board)
        pattern = self.generate_attack_pattern()

        attackable = []
        for tile in pattern:
            tile_unit = board.get_unit(tile[0], tile[1])
            if tile_unit != None:
                if tile_unit.health > 0 and tile_unit.player:
                    attackable.append(board.get_unit(tile[0], tile[1]))


        # always attack or defend if player within attackable squares, else move in a random direction
        if len(attackable) > 0:
            action = random.random()
            if action > 0.25: #attack
                player_choice = random.choice(attackable)
                return player_choice.take_damage(self)
            else:
                self.defend = True
                return f"{self.unit} at ({self.x+1},{self.y+1}) has defended"

        for i in range(self.action_count):
            # if there is a player within 5 squares then set to target unit
            if len(adjacents[2] + adjacents[3] + adjacents[4] + adjacents[5]) > 0 and self.target == None:
                self.target = random.choice(adjacents[2] + adjacents[3] + adjacents[4] + adjacents[5])

            # move one square along generated path towawrds target
            if self.target != None:
                path = self.create_path(board, self.target)
                if len(path) > 0: 
                    loc = path[0]
                    direction = (loc[0]-self.x, loc[1]-self.y)
                    self.move(board, direction)

            # return if final iteration
            if i == self.action_count-1: return ai_update

        self.move(board, random.choice(directions))
        return ai_update

# ========= Player Units ==============

class Knight(PartyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.BLUE}K{Style.RESET_ALL}"
        self.death_repr = f"{Fore.BLUE}{Style.DIM}x{Style.RESET_ALL}" # shows once unit killed
        self.unit = "Knight"
        self.health = 3
        self.damage = 2

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0)
        ]

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles] # simply add each relative directional modifier to current position

class Cavalry(PartyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.BLUE}C{Style.RESET_ALL}"
        self.death_repr = f"{Fore.BLUE}{Style.DIM}x{Style.RESET_ALL}" # shows once unit killed
        self.unit = "Cavalry"
        self.health = 2
        self.damage = 2
        self.action_count = 2
        self.base_action_count = 2

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0)
        ]

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles] # simply add each relative directional modifier to current position

class Archer(PartyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.BLUE}A{Style.RESET_ALL}"
        self.death_repr = f"{Fore.BLUE}{Style.DIM}x{Style.RESET_ALL}"
        self.unit = "Archer"
        self.health = 1
        self.damage = 2

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0),
        ]

        tiles = [(t[0]*(i+2), t[1]*(i+2)) for t in tiles for i in range(2)] # multiply each direction to add linear directional range and replace inner circle

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles]


# ========= Enemy Units ==============

class Bat(EnemyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.RED}B{Style.RESET_ALL}"
        self.death_repr = f"{Fore.RED}{Style.DIM}x{Style.RESET_ALL}"
        self.unit = "Bat"
        self.health = 1
        self.damage = 1

        self.action_count = 2

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0)
        ]

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles] # simply add each relative directional modifier to current position

class EnemyArcher(EnemyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.RED}A{Style.RESET_ALL}"
        self.death_repr = f"{Fore.RED}{Style.DIM}x{Style.RESET_ALL}"
        self.unit = "Enemy Archer"
        self.health = 1
        self.damage = 1
        self.action_count = 1

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0),
        ]

        tiles = [(t[0]*(i+2), t[1]*(i+2)) for t in tiles for i in range(2)] # multiply each direction to add linear directional range and replace inner circle

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles]

class EnemyKnight(EnemyUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.repr = f"{Fore.RED}K{Style.RESET_ALL}"
        self.death_repr = f"{Fore.RED}{Style.DIM}x{Style.RESET_ALL}" # shows once unit killed
        self.unit = "Enemy Knight"
        self.health = 3
        self.damage = 2

    def generate_attack_pattern(self):
        tiles = [
            (-1,-1), (0,-1), (1,-1),
            (-1,1), (0,1), (1,1),
            (-1,0), (1,0)
        ]

        return [(self.x+tile[0], self.y+tile[1]) for tile in tiles] # simply add each relative directional modifier to current position
