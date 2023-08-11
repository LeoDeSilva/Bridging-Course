from World import World
import random


def generate_interior(room_count, floor_screen, inaccessible_screen, items=None):
    if items is None:
        items = []

    neighbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # size of grid to place tiles, (will be collapsed later to fit size of generated dungeon
    width = 20
    height = 20

    # place initial room in center of grid thus room for expansion in all directions
    x, y = width//2, height//2
    room_locations = [(x, y)]  # array of coordinates of room locations

    for _ in range(room_count):
        neighbour_count = 0

        # while room position is not outside bounds, is not already occupied and not adjacent to >=2 other rooms
        while not 0 < x < width or not 0 < y < height or (x, y) in room_locations or not 0 < neighbour_count <= 1:
            # select position adjacent to existing room position
            x, y = random.choice(room_locations)
            direction = random.choice(neighbours)
            x += direction[0]
            y += direction[1] 

            # count number of occupied neighbour cells
            neighbour_count = 0
            for neighbour in neighbours:
                if (x+neighbour[0], y+neighbour[1]) in room_locations:
                    neighbour_count += 1

        room_locations.append((x, y))

    x_values = [r[0] for r in room_locations]  # all x and y positions of rooms to calculate min and max x and y values to min the grid
    y_values = [r[1] for r in room_locations]

    minx, maxx = min(x_values)-3, max(x_values)+4  # calculate min position with offset for a padded map image
    miny, maxy = min(y_values)-1, max(y_values)+2

    screens = [[inaccessible_screen(x, y, False) for x in range(maxx-minx)] for y in range(maxy-miny)]  # populate entire grid with inaccessible tiles

    for y in range(maxy-miny):
        for x in range(maxx-minx): 
            if (x+minx, y+miny) in room_locations:  # if tile meant to be occupied, replace inaccessible with a floor tile
                screens[y][x] = floor_screen(x, y, False)
                screens[y][x].visible = True

    world = World(maxx-minx, maxy-miny, screens)

    # determine random player starting position
    world.init_x, world.init_y = random.choice(room_locations)
    world.init_x -= minx
    world.init_y -= miny

    for item in items:  # select a random room to place each item into
        x, y = random.choice(room_locations)
        world.world[y-miny][x-minx].items.append(item)

    return world
