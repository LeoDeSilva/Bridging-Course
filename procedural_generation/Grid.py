from procedural_generation.Cell import Cell
import random


def intersection(a, b):
    return [element for element in a if element in b]


class Grid:
    def __init__(self, width, height, options):
        self.width = width
        self.height = height
        self.options = options  # stores all possible tile options composing terrain
        self.cells = []
        self.stack = []  # store cords of modified cells for propagating changes

    def instantiate(self):
        for y in range(self.height):
            self.cells.append([])
            for x in range(self.width):
                # assign each grid cell its initial maximum entropy state
                cell = Cell(x, y, self.options)
                self.cells[y].append(cell)

    def get_cell(self, x, y):
        for row in self.cells:
            for cell in row:
                if cell.x == x and cell.y == y:
                    return cell
        
        return None
    
    def get_cords(self, tile):
        for row in self.cells:
            for cell in row:
                if cell.options[0].index == tile:
                    return cell.x, cell.y

        return None

    def heuristic_pick(self):  # choose random cell from those with lowest entropy
        # shallow copy self.cells without reference
        cells_copy = [cell for row in self.cells for cell in row]

        # sort cells in order of entropy to determine lowest
        cells_copy = sorted(
            list(filter(lambda x: x.entropy() > 1, cells_copy)),
            key=lambda x: x.entropy(),
        )

        # store a list of the cells with the loosest entropy for heuristic selection
        lowest_entropy_cells = list(
            filter(lambda x: x.entropy() == cells_copy[0].entropy(), cells_copy)
        )

        return random.choice(lowest_entropy_cells)

    def is_collapsed(self):
        finished = True
        for row in self.cells:
            for cell in row:
                if not cell.collapsed:
                    finished = False

        return finished

    def is_valid_location(self, x, y):
        return not bool(x < 0 or x >= self.width or y < 0 or y >= self.height)

    def collect_adjacents(self, x, y):
        valid_options = []
        # print(x, y, [opt.valid_adjacents for opt in self.cells[x][y].options])
        for opt in self.cells[y][x].options:
            # print(opt.valid_adjacents, opt)
            valid_options.extend(opt.valid_adjacents)
        return valid_options

    # update valid adjacents and append to stack if changes
    def update_cell(self, x, y):
        if not self.is_valid_location(x, y):
            return

        if self.cells[y][x].collapsed:
            return

        central_cell = self.cells[y][x]
        cumulative_options = [opt for opt in central_cell.options]

        # print("CELL", x, y, cumulative_options)

        if self.is_valid_location(x, y - 1):
            valid_adjacents = self.collect_adjacents(x, y - 1)
            cumulative_options = intersection(cumulative_options, valid_adjacents)

        if self.is_valid_location(x, y + 1):
            valid_adjacents = self.collect_adjacents(x, y + 1)
            cumulative_options = intersection(cumulative_options, valid_adjacents)

        if self.is_valid_location(x - 1, y):
            valid_adjacents = self.collect_adjacents(x - 1, y)
            cumulative_options = intersection(cumulative_options, valid_adjacents)

        if self.is_valid_location(x + 1, y):
            valid_adjacents = self.collect_adjacents(x + 1, y)
            cumulative_options = intersection(cumulative_options, valid_adjacents)

        if cumulative_options != [opt for opt in central_cell.options]:
            self.stack.append((x, y))

        central_cell.options = cumulative_options
        central_cell.update()

    def compare(self, x, y, tile):
        if not self.is_valid_location(x, y):
            return False

        if self.cells[y][x].options[0] == tile:
            return True

    def count(self, tile):
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.options[0].index == tile:
                    count += 1

        return count

    def propagate(self):  # modify neighbours of changed cell
        while len(self.stack) != 0:
            (x, y) = self.stack[-1]

            self.update_cell(x, y - 1)  # up
            self.update_cell(x, y + 1)  # down
            self.update_cell(x - 1, y)  # left
            self.update_cell(x + 1, y)  # right

            self.stack.pop()

    def __str__(self):
        out_str = ""

        for row in self.cells:
            for cell in row:
                out_str += cell.__str__()
            out_str += "\n"

        return out_str
