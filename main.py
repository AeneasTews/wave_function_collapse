import random
from copy import deepcopy
import pickle
from PIL import Image, ImageDraw
import sys


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.states = [k for k in keys]
        self.entropy = len(self.states)
        self.collapsed = False

    def collapse(self):
        self.set_states([random.choice(self.states)])
        self.collapsed = True

    def set_states(self, states):
        self.states = states
        self.entropy = len(self.states)
        if self.entropy == 1:
            self.collapsed = True

    def remove_state(self, state):
        self.states.remove(state)
        self.entropy = len(self.states)
        if self.entropy == 1:
            self.collapsed = True


def generate_grid(dimension):
    grid = {}
    for y in range(dimension):
        for x in range(dimension):
            grid[f"{x} {y}"] = Tile(x, y)

    return grid


def least_entropy(grid):
    lowest_entropy = NUM_STATES
    for tile in grid.values():
        if 1 < len(tile.states) < lowest_entropy:
            lowest_entropy = len(tile.states)

    tiles = [tile for tile in filter(lambda tile: tile.entropy == lowest_entropy, grid.values())]
    return random.choice(tiles)


def collapse_tile(grid, tile):
    # choose tile
    tile.collapse()
    grid[f"{tile.x} {tile.y}"] = tile
    return grid


def update_entropy(grid, dimension):
    # loop through every tile and update entropy
    for tile in grid.values():
        if tile.collapsed:
            continue

        # get the tiles neighbors
        x, y = tile.x, tile.y
        neighbors = {"LEFT": grid[f"{x - 1} {y}"] if x > 0 else None,
                     "RIGHT": grid[f"{x + 1} {y}"] if x < dimension - 1 else None,
                     "UP": grid[f"{x} {y - 1}"] if y > 0 else None,
                     "DOWN": grid[f"{x} {y + 1}"] if y < dimension - 1 else None}

        # loop through all rules and get all possible values for every direction
        possible_states = {}
        for rule in rules:
            if not neighbors[rule[0]]:
                continue

            if not neighbors[rule[0]].states.__contains__(rule[1]):
                continue

            if possible_states.keys().__contains__(rule[0]):
                if not possible_states[rule[0]].__contains__(rule[2]):
                    possible_states[rule[0]].append(rule[2])
            else:
                possible_states[rule[0]] = [rule[2]]

        # print(f"possible_states for {tile.x}, {tile.y}: {possible_states}")  # debug
        # get the intersection of the possible values
        tile.set_states(get_intersection(possible_states))

    return grid


def get_intersection(possible_states):
    if len(possible_states) == 0:
        raise Exception("Impossible, please start from beginning")

    intersection = [k for k in keys]
    for direction in possible_states.keys():
        intersection = [state for state in possible_states[direction] if state in intersection]

    return intersection


def is_collapsed(grid):
    for tile in grid.values():
        if not tile.collapsed:
            return False

    return True


def compare_values(old_grid, grid):
    for y in range(DIM):
        for x in range(DIM):
            if old_grid[f"{x} {y}"].states != grid[f"{x} {y}"].states:
                return False

    return True


def collapse_grid(grid):
    #while not is_collapsed(grid):
    old_grid = deepcopy(grid)
    print("Updating Entropy...")  # Debug
    grid = update_entropy(grid, DIM)
    _debug_print_grid(grid)

    while not is_collapsed(grid):
        while not compare_values(old_grid, grid):
            old_grid = deepcopy(grid)
            print("Updating Entropy...")  # Debug
            grid = update_entropy(grid, DIM)
            _debug_print_grid(grid)

        if is_collapsed(grid):
            continue

        print("Collapsing tile...")  # Debug
        grid = collapse_tile(grid, least_entropy(grid))
        _debug_print_grid(grid)

    return grid


def final_print(grid):
    if not is_collapsed(grid):
        raise Exception("Grid is not fully collapsed!")

    for y in range(DIM):
        for x in range(DIM):
            print(colors[grid[f"{x} {y}"].states[0]], end="")
        print()


def output_image(grid, size, filename):
    # init
    p_size = size / DIM

    # create drawing context
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)

    for y in range(DIM):
        for x in range(DIM):
            draw.rectangle(((x * p_size, y * p_size), (x * p_size + p_size, y * p_size + p_size)),
                           fill=colors[grid[f"{x} {y}"].states[0]])

    img.save(filename)


def _debug_print_grid(grid):
    for y in range(DIM):
        for x in range(DIM):
            print(f"{grid[f"{x} {y}"].states}", end='')
        print()
    print()


def _debug_set_start_tile(grid, x, y, state):
    tile = Tile(x, y)
    tile.set_states(state)
    grid[f"{x} {y}"] = tile
    return grid


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Format main.py map_size rule_file color_scheme_file output_image")
        exit(1)

    # rules:
    # when checking the rules, a cell will retrieve all of its neighbors, these are represented by the directions
    # then it will check for every state of a neighbor and check which states cell itself can have according to this
    # neighbor. if a rule is violated. if this is case, the corresponding state will be removed from the possible states
    # the first value is the location of the neighbor, the second value is the state of the neighbor, and the third value is
    # the corresponding allowed state of the tile
    rules, keys = pickle.load(open(sys.argv[2], 'rb'))
    NUM_STATES = len(keys)

    # colors
    colors = {}
    try:
        colors = pickle.load(open(sys.argv[3], 'rb'))
        if not len(colors) == NUM_STATES:
            raise Exception("Invalid Color Key! Please ensure, that one color is defined for every key!")

    except FileNotFoundError:
        for key in keys:
            colors[key] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # colors = {
    #    0: '\033[32mL\033[0m',
    #    1: '\033[93mC\033[0m',
    #    2: '\033[34mS\033[34m',
    # }

    # initialize grid
    DIM = int(sys.argv[1])
    img_size = DIM * 10
    grid = generate_grid(DIM)
    _debug_print_grid(grid)  # Debug

    # collapse 1st tile
    #_debug_set_start_tile(grid, 2, 2, [SEA, SEA])
    collapse_tile(grid, least_entropy(grid))
    _debug_print_grid(grid)  # Debug

    # calculate entropy for every tile
    # update_entropy(grid, DIM)
    collapse_grid(grid)
    print("Final grid...")  # Debug
    _debug_print_grid(grid)

    # print the grid in color
    # final_print(grid)

    # generate an image based on grid
    output_image(grid, img_size, sys.argv[4])