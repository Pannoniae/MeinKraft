from PIL import Image

from .constants import *

def import_coords(x, y):
    # Converting image_process importing values to tex_coords methods.
    x = x * BLOCK_TEXTURE_SIZE
    y = y * BLOCK_TEXTURE_SIZE
    return x, y


def flip_image(img):
    " flip an image along the y axis"
    return img.transpose(Image.FLIP_TOP_BOTTOM)



def image_process():
    #Process the image files to texture.png at every program start.
    dirt = flip_image(Image.open(TEXTURE_PATH_DIRT))
    grass_side = flip_image(Image.open(TEXTURE_PATH_GRASS_SIDE))
    grass_top = flip_image(Image.open(TEXTURE_PATH_GRASS_TOP))
    sand = flip_image(Image.open(TEXTURE_PATH_SAND))
    brick = flip_image(Image.open(TEXTURE_PATH_BRICK))
    stone = flip_image(Image.open(TEXTURE_PATH_STONE))
    path_side = flip_image(Image.open(TEXTURE_PATH_PATH_SIDE))
    path_top = flip_image(Image.open(TEXTURE_PATH_PATH_TOP))

    # the origo for pixel coordinates is in the upper left corner
    texture = Image.new('RGBA', import_coords(4, 4), (0, 0, 0, 0))
    texture.paste(dirt, import_coords(0, 1))
    texture.paste(sand, import_coords(1, 1))
    texture.paste(stone, import_coords(2, 1))
    texture.paste(grass_side, import_coords(0, 0))
    texture.paste(grass_top, import_coords(1, 0))
    texture.paste(brick, import_coords(2, 0))
    texture.paste(path_side, import_coords(0, 2))
    texture.paste(path_top, import_coords(1, 2))
    # the origo of the texture coordinate system is at the lower left corner
    # flip the image
    texture = texture.transpose(Image.FLIP_TOP_BOTTOM)
    texture.save(imgpath('texture.png'))