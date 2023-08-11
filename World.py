from items.item import *
from combat.combat_handler import CombatHandler
from procedural_generation.generative_variables import *
from colorama import Style
from Player import Player
import random
import os


def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


class World:
    def __init__(self, width, height, screens):
        self.world = screens
        self.width = width
        self.height = height

        self.player = Player(world=self)
        self.scattered_items = []  # Items to be distributed randomly throughout the world (unique)

        self.running = True
        self.init_x, self.init_y = 0, 0

    def run(self):
        self.reveal_surrounding_tiles(self.player.x, self.player.y)
        while self.running:
            clear()
            screen = self.get_screen(self.player.x, self.player.y)

            if len(screen.hostiles) > 0: 
                if len(self.player.party) == 0: 
                    input("You have an empty party, recruit new units. proceed?")
                    self.player.recruit_cmd()

                combat_handler = CombatHandler(self, self.player.party, screen.hostiles)
                self.player.party = combat_handler.initialise_combat()
                screen.hostiles = []
                self.player.recruits = [random.choice(self.player.party_units)(None) for _ in range(4)]

            self.player.handle_input()

    def find(self, tile):
        for row in self.world:
            for screen in row:
                if screen.tile == tile:
                    return screen
        return None

    def get_screen(self, x, y):
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return None

        return self.world[y][x]
    
    def get_cords(self, tile):
        for row in self.world:
            for cell in row:
                if cell.tile == tile: 
                    return cell.x, cell.y

    def initialise(self): 
        # coordinates = self.generate_path(self.get_cords(START), self.get_cords(DUNGEON))
        for row in self.world:
            for screen in row:
                screen.populate()
                if screen.tile == START:
                    self.player.x = screen.x
                    self.player.y = screen.y

    def is_valid_location(self, x, y):  # determine whether given coordinate lies within grid
        return not bool(x < 0 or x >= self.width or y < 0 or y >= self.height)

    def reveal_surrounding_tiles(self, x, y):
        neighbours = [
            (x, y-1), (x, y+1), (x-1, y), (x+1, y),
            (x+1, y-1), (x+1, y+1), (x-1, y-1), (x-1, y+1)
        ]

        for neighbour_x, neighbour_y in neighbours:
            if self.is_valid_location(neighbour_x, neighbour_y):
                self.world[neighbour_y][neighbour_x].visible = True

    def __str__(self):
        out_str = f"{Fore.WHITE}#{Style.RESET_ALL}" * (self.width+2) + "\n"
        for row in self.world:
            out_str += f"{Fore.WHITE}#{Style.RESET_ALL}"
            for screen in row:
                if screen.x == self.player.x and screen.y == self.player.y:
                    out_str += self.player.__str__()
                else:
                    out_str += screen.__str__()
            out_str += f"{Fore.WHITE}#{Style.RESET_ALL}\n"

        out_str += f"{Fore.WHITE}#{Style.RESET_ALL}" * (self.width+2) + "\n"

        return out_str
