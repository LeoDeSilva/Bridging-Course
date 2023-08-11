from procedural_generation.Grid import Grid
from Screen import *
from World import World
import random


# replace random tile of type(s) locations with tile
def place_tile(grid, tile, locations):
    valid = False
    while not valid:
        x = random.randint(0, grid.width - 1)
        y = random.randint(0, grid.height - 1)

        # if selected tile is of desired type
        if grid.cells[y][x].options[0] in locations:
            grid.cells[y][x].options[0] = tile
            valid = True


# e.g. remove all sand tiles not adjacent to water (lifeline)
def remove_isolated_tiles(grid, tile, lifeline, replacement):
    for row in grid.cells:
        for cell in row:
            if cell.collapsed and cell.options[0] == tile:
                # if no adjacent squares are of the desired type - replace the cell
                if (
                    not grid.compare(cell.x, cell.y - 1, lifeline)
                    and not grid.compare(cell.x, cell.y + 1, lifeline)
                    and not grid.compare(cell.x - 1, cell.y, lifeline)
                    and not grid.compare(cell.x + 1, cell.y, lifeline)
                ):
                    cell.options[0] = replacement


# node for a_star pathfinding algorithm
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # distance from start (ie position in path)
        self.h = 0  # distance from end
        self.f = 0  # sum of both, low values indicate a shorter route heading towards the end

    def __eq__(self, other):
        return self.position == other.position 


def a_star_pathfinding(grid, start, finish):
    start_node = Node(None,  start)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, finish)
    end_node.g = end_node.h = end_node.f = 0

    open_list = [start_node]
    closed_list = []

    while len(open_list) > 0: 
        if len(open_list) > 50:
            return []  # should visited tiles exceed 1000 path does not exist

        current_node = open_list[0]
        current_index = 0

        # find lowest f value node in open cells
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:  # algorithm sold
            path = []
            current = current_node

            # traverse path backward via parent reference and update path state of corresponding grid cell
            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1]  # reverse path as collected backwards

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_pos = (current_node.position[0]+new_position[0], current_node.position[1]+new_position[1])
            neighbour_cell = grid.get_cell(node_pos[0], node_pos[1])

            if neighbour_cell and neighbour_cell.options[0].walkable:
                new_node = Node(current_node, node_pos)
                children.append(new_node)

        for child in children:  # if node previously calculated/visited : ignore
            for closed_child in closed_list:
                if closed_child == child:
                    continue

            child.g = current_node.g + 1

            # pythagoras to determine distance from current cell to end cell
            child.h = ((child.position[0]-end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:  # if the same cell in a more favourable path was visited : skip
                    continue

            open_list.append(child)

    return []


def migrate_wave_to_world(grid):
    screens = []
    screen_ids = {0: LandScreen, 1: ForrestScreen, 2: CoastScreen, 3: SeaScreen, 4: MountainScreen, 5: DungeonScreen, 6: BeginningScreen, 9: RuinsScreen}
    for row in grid.cells:
        screen_row = []
        for cell in row:
            if cell.options[0].index in screen_ids:
                screen_type = screen_ids[cell.options[0].index]
            else:
                screen_type = Screen

            screen_row.append(
                screen_type(
                    cell.x,
                    cell.y,
                    cell.path,
                )
            )
        screens.append(screen_row)

    world = World(grid.width, grid.height, screens)
    return world


def wave_function_collapse(width, height, options):
    grid = Grid(width, height, options)
    grid.instantiate()

    while not grid.is_collapsed():
        initial_cell = grid.heuristic_pick()
        initial_cell.collapse()  # collapse lowest entropy cell and propagate changes
        grid.stack.append((initial_cell.x, initial_cell.y))
        grid.propagate()
    # remove isolated coast tiles and insert Land Tile and Start Tile
    remove_isolated_tiles(grid, CoastTile, SeaTile, LandTile)
    place_tile(grid, StartTile, [LandTile])
    place_tile(grid, DungeonTile, [LandTile])
    place_tile(grid, RuinsTile, [LandTile])
    return grid


def create_world(width, height, options):
    grid = wave_function_collapse(width, height, options)
    dungeon_path = a_star_pathfinding(grid, grid.get_cords(START), grid.get_cords(DUNGEON))
    ruins_path = a_star_pathfinding(grid, grid.get_cords(START), grid.get_cords(RUINS))

    # distance to ruins between 5 and 10 tiles, dungeon > 10 tiles and ruins must be closer than dungeon
    while len(ruins_path) < 5 or len(ruins_path) > 10 or len(dungeon_path) < 10 or len(ruins_path) > len(dungeon_path) or grid.count(SEA) < 4:
        grid = wave_function_collapse(width, height, options)
        dungeon_path = a_star_pathfinding(grid, grid.get_cords(START), grid.get_cords(DUNGEON))
        ruins_path = a_star_pathfinding(grid, grid.get_cords(START), grid.get_cords(RUINS))

    world = migrate_wave_to_world(grid)
    world.initialise()
    return world
