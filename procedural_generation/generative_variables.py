from procedural_generation.Tile import Tile
from colorama import Fore

WIDTH = 16
HEIGHT = 8

LAND = 0
FORREST = 1
COAST = 2
SEA = 3
MOUNTAIN = 4
DUNGEON = 5
START = 6
WALL = 7
PATH = 8
RUINS = 9
DUNGEON_WALL = 10
DUNGEON_ROOM = 11

#   L F C S M
# L x x x - x
# F x x - - x
# C x - x x -
# S - - x x -
# M x x - - x

LandTile = Tile(LAND, ".", Fore.GREEN, 2.5, True)
ForrestTile = Tile(FORREST, "$", Fore.GREEN, 1.1, True)
SeaTile = Tile(SEA, "~", Fore.BLUE, 0.9, False)
CoastTile = Tile(COAST, "c", Fore.YELLOW, 0.9, True)
MountainTile = Tile(MOUNTAIN, "M", Fore.WHITE, 0.4, False)
DungeonTile = Tile(DUNGEON, "?", Fore.RED, 0, True)
RuinsTile = Tile(RUINS, "R", Fore.RED, 0, True)
StartTile = Tile(START, "B", Fore.RED, 0, True)
WallTile = Tile(WALL, "#", Fore.BLACK, 0, False)

RULES = [
    (LandTile, LandTile),
    (LandTile, ForrestTile),
    (LandTile, CoastTile),
    (LandTile, MountainTile),
    (ForrestTile, LandTile),
    (ForrestTile, ForrestTile),
    (ForrestTile, MountainTile),
    (CoastTile, LandTile),
    (CoastTile, CoastTile),
    (CoastTile, SeaTile),
    (SeaTile, CoastTile),
    (SeaTile, SeaTile),
    (MountainTile, LandTile),
    (MountainTile, ForrestTile),
    (MountainTile, MountainTile),
]
