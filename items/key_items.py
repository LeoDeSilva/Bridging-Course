from procedural_generation.generative_variables import RUINS
from colorama import Style
from items.item import *


class Map(Item):
    def __init__(self):
        super().__init__(MAP)

    def use(self, world):
        print(world)


class Compass(Item):
    def __init__(self):
        super().__init__(COMPASS)

    def use(self, world):
        ruins = world.find(RUINS)
        if not ruins:
            print("Cannot use that item here")
            return

        north = "N"
        south = "S"
        east = "E"
        west = "W"

        if world.player.y > ruins.y:
            north = f"{Style.BRIGHT}N{Style.RESET_ALL}"

        elif world.player.y < ruins.y:
            south = f"{Style.BRIGHT}S{Style.RESET_ALL}"

        if world.player.x < ruins.x:
            east = f"{Style.BRIGHT}E{Style.RESET_ALL}"

        elif world.player.x > ruins.x:
            west = f"{Style.BRIGHT}W{Style.RESET_ALL}"

        print("  " + north)
        print(west + f" {Style.BRIGHT}+{Style.RESET_ALL} " + east)
        print("  " + south)
