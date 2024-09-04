import pickle

BLANK = 0
T_UP = 1
T_RIGHT = 2
T_BOTTOM = 3
T_LEFT = 4
S_VERTICAL = 5
S_HORIZONTAL = 6

keys = {
    0: "BLANK",
    1: "T_UP",
    2: "T_RIGHT",
    3: "T_BOTTOM",
    4: "T_LEFT",
    5: "S_VERTICAL",
    6: "S_HORIZONTAL"
}
rules_dict = {
    BLANK: {
        "UP": [T_UP, BLANK, S_HORIZONTAL],
        "RIGHT": [T_RIGHT, BLANK, S_VERTICAL],
        "DOWN": [T_BOTTOM, BLANK, S_HORIZONTAL],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL]
    },
    T_RIGHT: {
        "UP": [T_LEFT, T_BOTTOM, T_RIGHT, S_VERTICAL],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL]
    },
    T_UP: {
        "UP": [T_LEFT, T_BOTTOM, S_VERTICAL],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL],
        "DOWN": [BLANK, T_BOTTOM, S_HORIZONTAL],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL]
    },
    T_LEFT: {
        "UP": [T_RIGHT, T_BOTTOM, T_LEFT, S_VERTICAL],
        "RIGHT": [BLANK, T_RIGHT, S_VERTICAL],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL]
    },
    T_BOTTOM: {
        "UP": [BLANK, T_UP, S_HORIZONTAL],
        "RIGHT": [T_UP, T_LEFT, T_BOTTOM, S_HORIZONTAL],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL]
    },
    S_VERTICAL: {
        "UP": [T_RIGHT, T_BOTTOM, T_LEFT, S_VERTICAL],
        "RIGHT": [T_RIGHT, BLANK, S_VERTICAL],
        "DOWN": [T_RIGHT, T_UP, T_LEFT, S_VERTICAL],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL]
    },
    S_HORIZONTAL: {
        "UP": [T_UP, BLANK, S_HORIZONTAL],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL],
        "DOWN": [T_BOTTOM, BLANK, S_HORIZONTAL],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL]
    }
}


def gen_rules(rules_dict):
    r = []

    for tile in rules_dict:
        for direction in rules_dict[tile]:
            for neighbor in rules_dict[tile][direction]:
                r.append((direction, neighbor, tile))

    return r


rules = gen_rules(rules_dict)

pickle.dump((rules, keys), open("tile_rules.pkl", "wb"))