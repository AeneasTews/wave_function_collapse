import random
from copy import deepcopy
import pickle
from PIL import Image
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

    return random.choice(tiles) if len(tiles) > 0 else None


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
    old_grid = deepcopy(grid)
    grid = update_entropy(grid, DIM)
    steps.append(get_current_image(grid, img_size))
    print(f"Progress: {(1 - ((get_total_entropy(grid)) / MAX_ENTROPY)) * 100:.2f}%")

    while not is_collapsed(grid):
        while not compare_values(old_grid, grid):
            old_grid = deepcopy(grid)
            grid = update_entropy(grid, DIM)
            steps.append(get_current_image(grid, img_size))  # Cooler looking progress gif
            print(f"Progress: {(1 - ((get_total_entropy(grid)) / MAX_ENTROPY)) * 100:.2f}%")

        if is_collapsed(grid):
            continue

        # steps.append(get_current_image(grid, img_size))  # Technically more accurate representation of progress
        next_tile = least_entropy(grid)
        if not next_tile:
            return None

        grid = collapse_tile(grid, least_entropy(grid))
        steps.append(get_current_image(grid, img_size))
        print(f"Progress: {(1 - ((get_total_entropy(grid)) / MAX_ENTROPY)) * 100:.2f}%")

    return grid


def get_total_entropy(grid):
    entropy = 0
    for tile in grid.values():
        entropy += tile.entropy

    return entropy - DIM * DIM


def output_image(grid, size, filename):
    print("Generating output image...")
    # create drawing context
    img = Image.new('RGB', (size, size))

    for y in range(DIM):
        for x in range(DIM):
            img.paste(tiles[grid[f"{x} {y}"].states[0]],
                      (x * t_size, y * t_size, x * t_size + t_size, y * t_size + t_size))

    img.save(filename)


def get_current_image(grid, size):
    # create drawing context
    img = Image.new('RGB', (size, size))

    for y in range(DIM):
        for x in range(DIM):
            if grid[f"{x} {y}"].entropy == NUM_STATES:
                tile = tiles[0]

            elif grid[f"{x} {y}"].collapsed:
                tile = tiles[grid[f"{x} {y}"].states[0]]

            else:
                tile = tiles[0]
                # color = get_average_color([colors[state] for state in grid[f"{x} {y}"].states])

            img.paste(tile, (x * t_size, y * t_size, x * t_size + t_size, y * t_size + t_size))

    return img


def output_gif(images, filename, loop=False, duration=50):
    print("Generating progress gif...")
    images[0].save(filename, save_all=True, append_images=images[1:], duration=duration, loop=loop)


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
    # randomness
    seed = random.randrange(0, sys.maxsize)
    random.seed(seed)

    # keep track of progress in order to create gif
    steps = []

    # rules:
    # when checking the rules, a cell will retrieve all of its neighbors, these are represented by the directions
    # then it will check for every state of a neighbor and check which states cell itself can have according to this
    # neighbor. if a rule is violated. if this is case, the corresponding state will be removed from the possible states
    # the first value is the location of the neighbor, the second value is the state of the neighbor, and the third value is
    # the corresponding allowed state of the tile
    rules, keys = pickle.load(open('tile_rules.pkl', 'rb'))
    NUM_STATES = len(keys)

    # initialize grid
    DIM = 20
    img_size = DIM * 100
    t_size = int(img_size / DIM)

    # tiles
    tiles = {}
    try:
        tile_paths = pickle.load(open("tile_scheme.pkl", 'rb'))
        for key in tile_paths:
            img = Image.open(tile_paths[key])
            img = img.resize((t_size, t_size))
            tiles[key] = img

        if not len(tiles) == NUM_STATES:
            raise Exception("Invalid Tile Key! Please ensure, that one key is defined for every tile!")

    except Exception as e:
        print(e)

    grid = generate_grid(DIM)
    grid_bkp = deepcopy(grid)  # backup copy of the grid in case the algorithm runs into an impossibility
    MAX_ENTROPY = DIM * DIM * NUM_STATES - DIM * DIM
    steps.append(get_current_image(grid, img_size))
    print(f"Progress: {(1 - ((get_total_entropy(grid)) / MAX_ENTROPY)) * 100:.2f}%")

    # collapse 1st tile
    collapse_tile(grid, least_entropy(grid))
    steps.append(get_current_image(grid, img_size))
    print(f"Progress: {(1 - ((get_total_entropy(grid)) / MAX_ENTROPY)) * 100:.2f}%")

    # collapse the grid
    grid = collapse_grid(grid)
    while grid is None:
        print("Contradiction detected!\nStarting again...")
        grid = deepcopy(grid_bkp)
        grid = collapse_grid(grid)

    # generate an image based on grid
    output_image(grid, img_size, ".\\output\\image.png")

    # generate output gif to show progress
    output_gif(steps, ".\\output\\progress.gif")

    print(f"Seed: {seed}")
