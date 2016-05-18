# config variables

import math

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(3 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

TEXTURE_PATH = 'texture.png'
TEXTURE_PATH_DIRT = 'dirt.png'
TEXTURE_PATH_GRASS_SIDE = 'grass_side.png'
TEXTURE_PATH_GRASS_TOP = 'grass_top.png'
TEXTURE_PATH_SAND = 'sand.png'
TEXTURE_PATH_BRICK = 'brick.png'
TEXTURE_PATH_STONE = 'stone.png'
