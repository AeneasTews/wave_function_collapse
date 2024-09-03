import pickle
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Format create_color_scheme.py rule_file output_file")
        exit(1)

    _, keys = pickle.load(open(sys.argv[1], "rb"))

    colors = {}
    for key in keys:
        color = [int(c) for c in input(f"Please enter color for {key}:{keys[key]}\n"
                                       f"format: red, green, blue:").replace(" ", "").split(",")]
        colors[key] = (color[0], color[1], color[2])
        print(f"\nPicked {colors[key]} for {key}:{keys[key]}\n")

    for color in colors:
        print(f"{color}: {colors[color]}")

    pickle.dump(colors, open(sys.argv[2], "wb"))
