from PIL import Image

from .constants import *

BLOCK_SIZE = 64
def import_coords(x, y):
    # Converting image_process importing values to tex_coords methods.
    x = x * BLOCK_SIZE
    y = y * BLOCK_SIZE
    return x, y

def image_process():
    #Process the image files to texture.png at every start.
    dirt = Image.open(TEXTURE_PATH_DIRT)
    grass_side = Image.open(TEXTURE_PATH_GRASS_SIDE)
    grass_top = Image.open(TEXTURE_PATH_GRASS_TOP)
    sand = Image.open(TEXTURE_PATH_SAND)
    brick = Image.open(TEXTURE_PATH_BRICK)
    stone = Image.open(TEXTURE_PATH_STONE)

    texture = Image.new('RGB', import_coords(4, 4))
    texture.paste(dirt, import_coords(0, 2))
    texture.paste(sand, import_coords(1, 2))
    texture.paste(stone, import_coords(2, 2))
    texture.paste(grass_side, import_coords(0, 3))
    texture.paste(grass_top, import_coords(1, 3))
    texture.paste(brick, import_coords(2, 3))
    texture.transpose(Image.FLIP_TOP_BOTTOM)
    texture.save(fixpath('texture.png'))