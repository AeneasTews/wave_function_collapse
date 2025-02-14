import pickle

BLANK = 0
T_UP = 1
T_RIGHT = 2
T_BOTTOM = 3
T_LEFT = 4
S_VERTICAL = 5
S_HORIZONTAL = 6
C_BOTTOM_LEFT = 7
C_LEFT_TOP = 8
C_TOP_RIGHT = 9
C_RIGHT_BOTTOM = 10

keys = {
    0: "BLANK",
    1: "T_UP",
    2: "T_RIGHT",
    3: "T_BOTTOM",
    4: "T_LEFT",
    5: "S_VERTICAL",
    6: "S_HORIZONTAL",
    7: "C_BOTTOM_LEFT",
    8: "C_LEFT_TOP",
    9: "C_TOP_RIGHT",
    10: "C_RIGHT_BOTTOM"
}
rules_dict = {
    BLANK: {
        "UP": [T_UP, BLANK, S_HORIZONTAL, C_LEFT_TOP, C_TOP_RIGHT],
        "RIGHT": [T_RIGHT, BLANK, S_VERTICAL, C_TOP_RIGHT, C_RIGHT_BOTTOM],
        "DOWN": [T_BOTTOM, BLANK, S_HORIZONTAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL, C_BOTTOM_LEFT, C_LEFT_TOP]
    },
    T_RIGHT: {
        "UP": [T_LEFT, T_BOTTOM, T_RIGHT, S_VERTICAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL, C_BOTTOM_LEFT, C_LEFT_TOP],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL, C_LEFT_TOP, C_BOTTOM_LEFT]
    },
    T_UP: {
        "UP": [T_LEFT, T_BOTTOM, S_VERTICAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL, C_BOTTOM_LEFT, C_LEFT_TOP],
        "DOWN": [BLANK, T_BOTTOM, S_HORIZONTAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_TOP_RIGHT, C_RIGHT_BOTTOM]
    },
    T_LEFT: {
        "UP": [T_RIGHT, T_BOTTOM, T_LEFT, S_VERTICAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "RIGHT": [BLANK, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_RIGHT_BOTTOM],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_RIGHT_BOTTOM, C_TOP_RIGHT]
    },
    T_BOTTOM: {
        "UP": [BLANK, T_UP, S_HORIZONTAL, C_LEFT_TOP, C_TOP_RIGHT],
        "RIGHT": [T_UP, T_LEFT, T_BOTTOM, S_HORIZONTAL, C_BOTTOM_LEFT, C_LEFT_TOP],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_RIGHT_BOTTOM, C_TOP_RIGHT]
    },
    S_VERTICAL: {
        "UP": [T_RIGHT, T_BOTTOM, T_LEFT, S_VERTICAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "RIGHT": [T_RIGHT, BLANK, S_VERTICAL, C_TOP_RIGHT, C_RIGHT_BOTTOM],
        "DOWN": [T_RIGHT, T_UP, T_LEFT, S_VERTICAL, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL, C_BOTTOM_LEFT, C_LEFT_TOP]
    },
    S_HORIZONTAL: {
        "UP": [T_UP, BLANK, S_HORIZONTAL, C_LEFT_TOP, C_TOP_RIGHT],
        "RIGHT": [T_BOTTOM, T_LEFT, T_UP, S_HORIZONTAL, C_LEFT_TOP, C_BOTTOM_LEFT],
        "DOWN": [T_BOTTOM, BLANK, S_HORIZONTAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_RIGHT_BOTTOM, C_TOP_RIGHT]
    },
    C_BOTTOM_LEFT: {
        "UP": [BLANK, T_UP, S_HORIZONTAL, C_LEFT_TOP, C_TOP_RIGHT],
        "RIGHT": [BLANK, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_RIGHT_BOTTOM],
        "DOWN": [T_LEFT, T_UP, T_RIGHT, S_VERTICAL, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_TOP_RIGHT, C_RIGHT_BOTTOM]
    },
    C_LEFT_TOP: {
        "UP": [T_RIGHT, T_BOTTOM, T_LEFT, S_VERTICAL, C_BOTTOM_LEFT, C_RIGHT_BOTTOM],
        "RIGHT": [BLANK, S_VERTICAL, T_RIGHT, C_TOP_RIGHT, C_RIGHT_BOTTOM],
        "DOWN": [BLANK, S_HORIZONTAL, T_BOTTOM, C_RIGHT_BOTTOM, C_BOTTOM_LEFT],
        "LEFT": [T_UP, T_RIGHT, T_BOTTOM, S_HORIZONTAL, C_RIGHT_BOTTOM, C_TOP_RIGHT]
    },
    C_TOP_RIGHT: {
        "UP": [S_VERTICAL, T_RIGHT, T_BOTTOM, T_LEFT, C_RIGHT_BOTTOM, C_BOTTOM_LEFT],
        "RIGHT": [S_HORIZONTAL, T_BOTTOM, T_LEFT, T_UP, C_LEFT_TOP, C_BOTTOM_LEFT],
        "DOWN": [BLANK, S_HORIZONTAL, C_RIGHT_BOTTOM, C_BOTTOM_LEFT, T_BOTTOM],
        "LEFT": [T_LEFT, BLANK, S_VERTICAL, C_LEFT_TOP, C_BOTTOM_LEFT]
    },
    C_RIGHT_BOTTOM: {
        "UP": [S_HORIZONTAL, BLANK, T_UP, C_LEFT_TOP, C_TOP_RIGHT],
        "RIGHT": [S_HORIZONTAL, T_BOTTOM, T_LEFT, T_UP, C_LEFT_TOP, C_BOTTOM_LEFT],
        "DOWN": [S_VERTICAL, T_LEFT, T_UP, T_RIGHT, C_TOP_RIGHT, C_LEFT_TOP],
        "LEFT": [BLANK, S_VERTICAL, T_LEFT, C_BOTTOM_LEFT, C_LEFT_TOP]
    },
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