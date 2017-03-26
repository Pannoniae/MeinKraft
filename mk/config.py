# config variables

import math
from .utils import base_path

TICKS_PER_SEC = 40
GAME_TICKS_PER_SEC = 10

# How many updates are called before fully switching zoom states.
ZOOM_STATES = 10

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15
BLOCK_TEXTURE_SIZE = 16
TEXTURE_PATH = base_path('texture.png')

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0  # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2
MAX_FOV = 80
MIN_FOV = 20

