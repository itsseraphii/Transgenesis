from pygame import Rect

HITBOX_SIZES = { # Defaults to 32x32 with 0x0 offset
    28: [16, 16, 7, 7],
    43: [32, 28, 0, 2],
    44: [32, 28, 0, 2],
    58: [32, 28, 0, 2],
    59: [32, 28, 0, 2],
    71: [26, 29, 4, 1],
    72: [30, 28, 1, 1],
    73: [32, 16, 0, 7],
    74: [16, 32, 7, 0],
    91: [32, 16, 0, 16],
    92: [32, 16, 0, 16],
    93: [20, 16, 12, 16],
    94: [20, 16, 0, 16],
    105: [28, 32, 2, 0],
    106: [28, 32, 2, 0],
    107: [28, 32, 2, 0],
    108: [28, 32, 2, 0]
}

RESISTANCES = { # Defaults to 2
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    8: 0,
    13: 3,
    15: 0,
    18: 0,
    19: 0,
    20: 0,
    25: 1,
    27: 1,
    28: 1,
    30: 0,
    33: 0,
    40: 1,
    42: 1,
    43: 0,
    44: 0,
    45: 0,
    46: 0,
    47: 0,
    48: 0,
    49: 0,
    50: 0,
    55: 1,
    58: 0,
    59: 0,
    62: 0,
    64: 0,
    65: 0,
    66: 0,
    72: 1,
    73: 0,
    74: 0,
    75: 1,
    77: 0,
    78: 0,
    79: 0,
    80: 0,
    81: 0,
    82: 0,
    83: 0,
    87: 0,
    103: 0,
    105: 0,
    106: 0,
    107: 0,
    108: 0,
    139: 0
}

class Obstacle:
    def __init__(self, resistance, posX, posY, hitbox):
        self.resistance = resistance # 0: blocks bodies  1: blocks low caliber  2: blocks high caliber  3: blocks everything
        self.posX = posX
        self.posY = posY
        self.hitbox = Rect(posX + hitbox[2], posY + hitbox[3], hitbox[0], hitbox[1])