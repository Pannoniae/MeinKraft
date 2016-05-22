from PIL import Image

from .constants import *

def import_coords(x, y):
    # Converting image_process importing values to tex_coords methods.
    x = x * BLOCK_TEXTURE_SIZE
    y = y * BLOCK_TEXTURE_SIZE
    return x, y

def flip_image(img):
    " flip an image along the y axis"
    new_img=Image.new("RGB",img.size)
    img_pixels, new_pixels = img.load(), new_img.load()
    x_size, y_size = img.size
    for x in xrange(x_size):
        for y in xrange(y_size):
            flipped_y = y_size - y - 1
            new_pixels[x, flipped_y] = img_pixels[x, y]

    return new_img



def image_process():
    #Process the image files to texture.png at every program start.
    dirt = flip_image(Image.open(TEXTURE_PATH_DIRT))
    grass_side = flip_image(Image.open(TEXTURE_PATH_GRASS_SIDE))
    grass_top = flip_image(Image.open(TEXTURE_PATH_GRASS_TOP))
    sand = flip_image(Image.open(TEXTURE_PATH_SAND))
    brick = flip_image(Image.open(TEXTURE_PATH_BRICK))
    stone = flip_image(Image.open(TEXTURE_PATH_STONE))

    # the origo for pixel coordinates is in the upper left corner
    texture = Image.new('RGB', import_coords(4, 4))
    texture.paste(dirt, import_coords(0, 1))
    texture.paste(sand, import_coords(1, 1))
    texture.paste(stone, import_coords(2, 1))
    texture.paste(grass_side, import_coords(0, 0))
    texture.paste(grass_top, import_coords(1, 0))
    texture.paste(brick, import_coords(2, 0))
    # the origo of the texture coordinate system is at the lower left corner
    # flip the image
    texture = texture.transpose(Image.FLIP_TOP_BOTTOM)
    texture.save(imgpath('texture.png'))