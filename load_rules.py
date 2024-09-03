import pickle
import sys

def load_grid(filename):
    # init
    grid = []
    with open(filename, 'r') as f:
        keys = assign_keys(f)

        with open(filename, 'r') as f:
            for line in f.readlines():
                grid.append([])
                for tile in line:
                    if tile != "\n":
                        grid[-1].append(keys[tile])

    # invert the key dict
    g_keys = {}

    for key in keys:
        g_keys[keys[key]] = key

    return grid, g_keys


def assign_keys(file):
    keys = {}
    for line in file.readlines():
        for tile in line:
            if keys.keys().__contains__(tile) or tile == "\n":
                continue

            keys[tile] = len(keys)

    return keys


def rules_from_tiles(grid):
    # create rule list
    rules = []

    # get the neighbors for every tile
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            neighbors = {"UP": grid[y - 1][x] if y > 0 else None,
                         "RIGHT": grid[y][x + 1] if x < len(grid[y]) - 1 else None,
                         "DOWN": grid[y + 1][x] if y < len(grid) - 1 else None,
                         "LEFT": grid[y][x - 1] if x > 0 else None}

            for direction in neighbors.keys():
                if neighbors[direction] is None:
                    continue

                rules.append((direction, neighbors[direction], tile))

    return list(set(rules))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Format load_rules.py input_file output_file")
        exit(1)

    grid, keys = load_grid(sys.argv[1])
    rules = rules_from_tiles(grid)
    pickle.dump((rules, keys), open(sys.argv[2], "wb"))
    print(f"Successfully created rule set '{sys.argv[2]}' from '{sys.argv[1]}'")
