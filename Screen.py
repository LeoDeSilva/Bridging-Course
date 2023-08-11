from procedural_dungeons.procedural_dungeon import generate_interior
from procedural_generation.generative_variables import *

from items.consumables import *
from items.key_items import *

from combat.units.hostile_units import *
from colorama import Fore, Style

import json
import random


class Screen:
    def __init__(self, x, y, path):
        self.tile = None
        self.char = None
        self.colour = None
        self.x = x
        self.y = y

        self.visited = False
        self.walkable = True
        self.visible = False
        self.entrance = False

        self.combat = False  # if combat should take place on this screen (dictated at initialisation)
        self.hostile_units = {  # available units for each party position
            0: [CorruptedKnight, Bat],
            1: [CorruptedKnight, Bat],
            2: [CorruptedArcher, CorruptedMonk],
            3: [CorruptedArcher, CorruptedMonk]
        }

        self.hostiles = []
        self.items = []
        self.potential_items = []  # list containing tuples of potential items and their rarity for a particular screen

        self.path = path
        self.bf_searched = False  # visited by BFS pathfinding algorithm

        self.access_msg = ""

        self.descriptors = {}
        self.load_descriptors()

    def load_descriptors(self):
        f = open('descriptors.json')
        self.descriptors = json.load(f)
        f.close()

    def populate(self):
        if self.combat:
            num_hostiles = random.randint(2, 4)
            for i in range(num_hostiles):
                self.hostiles.append(random.choice(self.hostile_units[i])(i))

        for item_tuple in self.potential_items:  # item and chance occurrence
            if random.random() < item_tuple[1]:
                self.items.append(item_tuple[0])

    def compass(self, c2):  # return direction of tile relative to self position
        direction = ""

        if c2[1] < self.y:
            direction += "north"
        elif c2[1] > self.y:
            direction += "south"

        if c2[0] > self.x:
            direction += "east"
        elif c2[0] < self.x:
            direction += "west"

        return direction

    def generate_surroundings_msg(self, world):
        surrounding_text = ""
        x, y = self.x, self.y
        neighbours = [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y),
                      (x - 1, y - 1)]
        surroundings = {}

        if len(self.items) > 0:  # loop through all items contained in screen and format into string
            surrounding_text += f"You see {', '.join([item.item for item in self.items])} on the ground\n"

        # group all neighbour cells by type
        for cell in neighbours:
            screen = world.get_screen(cell[0], cell[1])
            # TODO: mountains, oceans, ruins
            if screen:
                if screen.tile == 11 and (
                        self.x == screen.x or self.y == screen.y):  # if dungeon floor tile ignore diagonals
                    if screen.tile not in surroundings:
                        surroundings[screen.tile] = [screen]
                    else:
                        surroundings[screen.tile].append(screen)  # if existing tiles with key append to current list

                if screen.path and not (self.x != screen.x and self.y != screen.y):
                    if not surroundings[PATH]:
                        surroundings[PATH].append(screen)  # if existing tiles with key append to current list
                    else:
                        surroundings[PATH] = [screen]  # otherwise initialise the list

        for key in surroundings:
            # join all directions of adjacent tiles with a comma ("north, south, south west")
            direction_txt = ", ".join(
                [self.compass((surroundings[key][i].x, surroundings[key][i].y)) for i in range(len(surroundings[key]))])

            match key:
                case 1:
                    surrounding_text += f"{Style.BRIGHT}Forests {Style.RESET_ALL}{Style.DIM}lie {Style.NORMAL}" + direction_txt + f"{Style.DIM} of you.{Style.RESET_ALL}"
                case 2:
                    surrounding_text += f"{Style.DIM}You can see {Style.RESET_ALL}{Style.BRIGHT}riverbanks{Style.RESET_ALL}{Style.DIM} to your {Style.NORMAL}" + direction_txt + f".{Style.RESET_ALL}"
                case 3:
                    surrounding_text += f"{Style.BRIGHT}Rivers{Style.RESET_ALL}{Style.DIM} span {Style.NORMAL}" + direction_txt + f".{Style.RESET_ALL}"
                case 4:
                    surrounding_text += f"{Style.BRIGHT}Mountains{Style.RESET_ALL}{Style.DIM} reach {Style.NORMAL}" + direction_txt + f".{Style.RESET_ALL}"
                case 5:
                    surrounding_text += f"{Fore.RED}{Style.BRIGHT}To your " + direction_txt + f" you hear a voice.{Style.RESET_ALL}"
                case 8:
                    surrounding_text += f"{Fore.LIGHTYELLOW_EX}A path lies to your " + direction_txt + f".{Style.RESET_ALL}"  # path
                case 11:
                    surrounding_text += f"{Style.BRIGHT}Doorways {Style.RESET_ALL}{Style.DIM}lie to your {Style.NORMAL}{direction_txt}{Style.RESET_ALL}"

            surrounding_text += '\n'

        return surrounding_text

    def generate_msg(self, terrain):
        preceeder = random.choice(self.descriptors["preceeders"])  # you walk into, you come across a
        adjective = random.choice(self.descriptors[terrain]["adjective"])  # dense, lush
        location = random.choice(self.descriptors[terrain]["location_type"])  # mountain, forrest
        feature = ""

        # chose between 0-2 detailed descriptions of location
        for _ in range(random.randint(0, 2)):
            selection = random.choice(self.descriptors[terrain]["feature"])
            if selection not in feature:
                feature += selection + " "

        return preceeder + " a " + adjective + f" {self.colour}" + location + f"{Style.RESET_ALL}.\n" + feature[:-1]

    def __str__(self):
        if self.path:
            return (
                f"{Fore.WHITE}{self.char}{Style.RESET_ALL}"
                if self.visible
                else f"{Fore.BLACK}?{Style.RESET_ALL}"
            )

        return (
            f"{self.colour}{self.char}{Style.RESET_ALL}"
            if self.visible or self.tile in (DUNGEON, RUINS)
            else f"{Fore.BLACK}?{Style.RESET_ALL}"
        )


class LandScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
        self.tile = LAND
        self.char = "."
        self.colour = Fore.GREEN

        self.potential_items = [
            (Berry(), 0.2),
        ]

        self.access_msg = self.generate_msg("land")
        self.combat = random.random() < 0.5

    def accessed_msg(self):
        return self.access_msg if not self.visited else "Plain"


class ForrestScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)
        self.tile = FORREST
        self.char = "$"
        self.colour = Fore.GREEN

        self.potential_items = [
            (Berry(), 0.5),
        ]

        self.access_msg = self.generate_msg("forrest")
        self.combat = random.random() < 0.50

    def accessed_msg(self):
        return self.access_msg if not self.visited else "Forrest"


class CoastScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = COAST
        self.char = "c"
        self.colour = Fore.YELLOW

        self.access_msg = self.generate_msg("coast")
        self.combat = random.random() < 0.2

    def accessed_msg(self):
        return self.access_msg if not self.visited else "Coast"


class SeaScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = SEA
        self.char = "~"
        self.colour = Fore.BLUE

        self.access_msg = self.generate_msg("sea")
        self.walkable = False
        self.inaccessible_msg = "You would need a boat to cross the river"

    def accessed_msg(self):
        return self.access_msg if not self.visited else "Ocean"


class MountainScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = MOUNTAIN
        self.char = "M"
        self.colour = Fore.WHITE

        self.access_msg = self.generate_msg("mountain")
        self.walkable = False
        self.inaccessible_msg = "Your way is blocked by impenetrable mountains"

    def accessed_msg(self):
        return self.access_msg if not self.visited else "Mountain"


class DungeonRoom(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = DUNGEON_ROOM
        self.char = "x"
        self.colour = Fore.WHITE

        self.access_msg = self.generate_msg("dungeon_room")
        self.combat = random.random() > 0.5

    def accessed_msg(self):
        return self.access_msg


class DungeonWall(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = DUNGEON_WALL
        self.char = "?"
        self.colour = Fore.BLACK

        self.access_msg = self.generate_msg("dungeon_wall")
        self.walkable = False
        self.inaccessible_msg = "No path leads in that direction"

    def accessed_msg(self):
        return self.access_msg


class BeginningScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = START
        self.char = "B"
        self.colour = Fore.RED

        self.access_msg = self.generate_msg("building")
        self.visited = True
        self.entrance = True

        self.dungeon = generate_interior(0, DungeonRoom, DungeonWall, [Compass()])

    def accessed_msg(self):
        return self.access_msg


class DungeonScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = DUNGEON
        self.char = "D"
        self.colour = Fore.RED

        self.access_msg = self.generate_msg("dungeon")
        self.entrance = True
        self.dungeon = generate_interior(10, DungeonRoom, DungeonWall)

    def accessed_msg(self):
        return self.access_msg


class RuinsScreen(Screen):
    def __init__(self, x, y, path):
        super().__init__(x, y, path)

        self.tile = RUINS
        self.char = "R"
        self.colour = Fore.RED

        self.access_msg = self.generate_msg("ruins")
        self.entrance = True
        self.dungeon = generate_interior(10, DungeonRoom, DungeonWall, [Map()])

    def accessed_msg(self):
        return self.access_msg
