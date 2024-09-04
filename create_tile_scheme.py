import pickle
import os

if __name__ == "__main__":
    path = os.path.join(os.path.abspath(__file__), "..")

    _, keys = pickle.load(open("tile_rules.pkl", "rb"))

    tiles = {}
    for key in keys:
        tile = os.path.join(path, input(f"Please enter path for {key}:{keys[key]}:"))
        tiles[key] = tile
        with open(tile, "r") as f:
            print(f"\nPicked file {tiles[key]} for {key}:{keys[key]}\n")

    for tile in tiles:
        print(f"{tile}: {tiles[tile]}")

    pickle.dump(tiles, open("tile_scheme.pkl", "wb"))