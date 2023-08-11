import random 
from colorama import Fore, Style
import os

#TODO: action count, if wait, action count += 1 

class Board:
    def __init__(self, screen, player, enemies):
        self.screen = screen
        self.playerRef = player
        self.enemiesRef = enemies

        self.playerUnits = []
        self.enemyUnits = []

        self.size = 9
        self.board = [[0 for i in range(self.size)] for i in range(self.size)]

    def clear(self):
        if os.name == "posix": os.system("clear")
        else: os.system("cls")

    def generate_obstacles(self, number):
        for i in range(number):
            wall = [1, random.randint(2, 5)]
            # generate start x,y position limited thus wall cannot exceed board boundaries
            startx, starty = random.randint(1, (self.size-1)-wall[0]), random.randint(1,self.size-1-wall[1])
            random.shuffle(wall)

            for y in range(wall[1]):
                for x in range(wall[0]):
                    if self.is_valid_location((startx+x, starty+y)):
                        self.board[starty+y][startx+x] = 1

    def initalise(self):
        self.generate_obstacles(random.randint(2,5))
        split = random.choice(["horizontal", "vertical"])

        # determine spawnable range for enemies (either horizontally or vertically split)
        for e in self.enemiesRef:
            if split == "horizontal": loc = (random.randint(0,(self.size-1)//2), random.randint(0,self.size-1))
            elif split == "vertical": loc = (random.randint(0,self.size-1), random.randint(0,(self.size-1)//2))

            while self.occupied(loc) or not self.is_valid_location(loc): 
                if split == "horizontal": loc = (random.randint(0,(self.size-1)//2), random.randint(0,self.size-1))
                elif split == "vertical": loc = (random.randint(0,self.size-1), random.randint(0,(self.size-1)//2))

            self.enemyUnits.append(e(loc[0], loc[1]))

        for p in self.playerRef.party:
            if split == "horizontal": loc = (random.randint((self.size-1)//2, self.size-1), random.randint(0,self.size-1))
            elif split == "vertical": loc = (random.randint(0,self.size-1), random.randint((self.size-1)//2, self.size-1))

            while self.occupied(loc) or not self.is_valid_location(loc): 
                if split == "horizontal": loc = (random.randint((self.size-1)//2, self.size-1), random.randint(0,self.size-1))
                elif split == "vertical": loc = (random.randint(0,self.size-1), random.randint((self.size-1)//2, self.size-1))

            self.playerUnits.append(p(loc[0], loc[1]))


    def occupied(self, location): # determine whether unit already occupies square
        for unit in self.playerUnits + self.enemyUnits:
            if unit.x == location[0] and unit.y == location[1]:
                return True
        return False

    def get_cell(self, x, y):
        if self.is_valid_location((x,y)):
            return self.board[y][x]
        return None

    def get_unit(self, x, y):
        units = []
        for unit in self.playerUnits + self.enemyUnits:
            if unit.x == x and unit.y == y:
                units.append(unit)

        if len(units) == 0: return None

        if len(units) > 1:
            for unit in units: 
                if not unit.hidden: return unit

        return units[0]

    def is_valid_location(self, loc):
        x, y = loc
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False

        if self.board[loc[1]][loc[0]] != 0: # if tile is not floor (e.g. trap or wall) then not movable 
            return False
        return True

    def compile(self, a, b): # add two coordinates
        return [a[0]+b[0], a[1]+b[1]]

    def begin_combat(self):
        self.running = True

        # while running and at least one enemy is alive (health > 0)
        while self.running and len(list(filter(lambda u: u.health > 0, self.enemyUnits))) > 0:
            self.handle_input()
            self.handle_enemy_ai()

        # clear screen and remove all enemies (perhaps exemption if flees)
        if len(list(filter(lambda u: u.health > 0, self.enemyUnits))) <= 0:
            print("You have felled all enemies")
            input("continue?")

        self.clear()
        self.screen.enemies = []

    def handle_enemy_ai(self):
        for enemy in self.enemyUnits:
            self.clear()

            enemy.turn = True
            enemy.defend = False
            update_txt = enemy.handle_ai(self)

            print(self)
            if update_txt != "":
                print(update_txt)
                input("continue?")

            enemy.turn = False

    def handle_input(self):
        for unit in self.playerUnits:
            if unit.health <= 0: continue

            self.clear()
            unit.turn = True
            unit.defend = False

            enemy_patterns = []
            for enemy in self.enemyUnits: 
                if enemy.health > 0:
                    enemy_patterns.extend(enemy.generate_attack_pattern())

            print(self.__str__(unit.generate_attack_pattern(), enemy_patterns)) # reprint grid with attackable squares
            print(f"({unit.x+1},{unit.y+1}) health: {unit.health}")

            unit.turn = False

            if unit.action_count == 0: unit.action_count = unit.base_action_count # reset action count 
            print(f"{unit.unit} has {unit.action_count} actions")

            skip = False
            while unit.action_count > 0 and not skip:
                if not self.running or len(list(filter(lambda u: u.health > 0, self.enemyUnits))) <= 0: return
                # quit if flee or no enemies are left alive

                cmd = ""
                while cmd == "":
                    cmd = input(unit.unit + ":")

                params = " ".join(cmd.split(" ")[1:])
                cmd = cmd.split(" ")[0]

                match cmd.split(" ")[0]:
                    case "go":
                        self.go_cmd(unit, params)
                    case "attack":
                        self.attack_cmd(unit, params)
                    case "defend":
                        unit.defend = True
                    case "run":
                        self.running = False
                        return
                    case "wait":
                        skip = True

                unit.action_count -= 1
                if unit.action_count > 0: # update ui for second action per turn
                    unit.turn = True
                    self.clear()
                    enemy_patterns = []
                    for enemy in self.enemyUnits: 
                        if enemy.health > 0:
                            enemy_patterns.extend(enemy.generate_attack_pattern())

                    print(self.__str__(unit.generate_attack_pattern(), enemy_patterns)) # reprint grid with attackable squares
                    print(f"You have {unit.action_count} actions remaining")
                    unit.turn = False

    
    def attack_cmd(self, unit, params):
        params = "".join(params.split(" ")) # remove all spaces
        pattern = unit.generate_attack_pattern() # create list of all attackable squares 

        found = False
        attack_coords = [unit.x, unit.y]

        while not found or not self.is_valid_location(attack_coords):
            attack_coords = [unit.x, unit.y]

            if "," not in params: # determine whether coordinate or direction was input
                match params:
                    case "north": attack_coords = self.compile(attack_coords, [0, -1]) 
                    case "south": attack_coords = self.compile(attack_coords, [0, 1]) 
                    case "east": attack_coords = self.compile(attack_coords, [1, 0]) 
                    case "west": attack_coords = self.compile(attack_coords, [-1, 0]) 
                    case "_": 
                        print("I don't recognise that direction: ", params)
                        continue
            else:
                coords = params.split(",")
                try: attack_coords = (int(coords[0])-1, int(coords[1])-1) # convert coordinate string into tuple
                except: print("Invalid coordinates entered: " + params)

            found = False
            for p in pattern:
                if p[0] == attack_coords[0] and p[1] == attack_coords[1]: 
                    found = True

            if not found or not self.is_valid_location(attack_coords): 
                print(f"Selected coordinates outside attack range: ({attack_coords[0]+1},{attack_coords[1]+1})")
                params = input("\nlocation:")

        # once coordinates determined : locate and damage unit
        target_unit = self.get_unit(attack_coords[0], attack_coords[1])
        if  target_unit != None: 
            if target_unit.health == 0: # if attacking a corpse, hide and thus remove obstruction
                target_unit.hidden = True
            else:
                out = target_unit.take_damage(unit)
                print(out)

            if unit.action_count == 0 or target_unit.health > 0:
                input("continue?")


    def go_cmd(self, unit, params):
        direction = (0,0)

        match params:
            case "north": direction = (0,-1)
            case "south": direction = (0,1)
            case "east": direction = (1,0)
            case "west": direction = (-1,0)
            case "_": print("Invalid direction entered: " + params)

        if not unit.move(self, direction):
            print(f"Invalid move location")
            input("continue?")

    def __str__(self, attack_pattern=[], enemy_patterns=[]):
        out = "  " + " ".join([str(x+1) for x in range(self.size)]) + "\n"
        for y in range(len(self.board)):
            out += str(y+1) + " "

            for x in range(len(self.board[y])):
                if self.board[y][x] == 1:
                    out += f"{Style.DIM}#{Style.RESET_ALL} "

                elif self.get_unit(x,y) != None and not self.get_unit(x,y).hidden:
                    if self.get_unit(x,y).health == 0:
                        out += self.get_unit(x,y).death_repr + " "
                    elif (x,y) in attack_pattern:
                        out += f"{Style.DIM}" + self.get_unit(x,y).__str__() + f" {Style.RESET_ALL}"
                    else:
                        out += self.get_unit(x,y).__str__() + " "

                #elif (x,y) in attack_pattern and (x,y) in enemy_patterns:
                #    out += f"{Fore.LIGHTRED_EX}o {Style.RESET_ALL}"
                elif (x,y) in attack_pattern:
                    out += f"{Style.DIM}o {Style.RESET_ALL}"
                elif (x,y) in enemy_patterns:
                    out += f"{Fore.LIGHTRED_EX}. {Style.RESET_ALL}"

                else:
                    out += f"{Style.DIM}.{Style.RESET_ALL} "
            out += "\n"
        return out
                
    

def initialise_combat(world,screen, player, enemies):
    board = Board(screen, player, enemies)

    board.clear()
    print(screen.accessed_msg())
    print(screen.generate_surroundings_msg(world))
    input("You are ambused by a patrol intialising a fierce combat.")

    board.initalise()
    board.begin_combat()