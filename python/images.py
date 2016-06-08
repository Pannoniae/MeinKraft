import os.path
import sys
import time

from PIL import Image

from .constants import BLOCK_TEXTURE_SIZE


def imgpath(filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "blockdata", filename)

TEXTURE_PATH = imgpath('texture.png')

def import_coords(x, y):
    # Converting image_process importing values to tex_coords methods.
    x = x * BLOCK_TEXTURE_SIZE
    y = y * BLOCK_TEXTURE_SIZE
    return x, y


def flip_image(img):
    """ flip an image along the y axis """
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def image_process():
    # Process the image files to texture.png at every program start.
    imgfile = []
    texture = Image.new('RGBA', import_coords(4, 4), (0, 0, 0, 0))
    imgdir = os.listdir('blockdata')
    files = len(imgdir)
    x = 0
    y = 0
    while x <= 4:
        while y <= 4:
            for fn in imgdir:
                fnpath = imgpath(fn)
                # print(globals()[fnpath])
                files -= 1
                if files < 0:
                    break
                fnimg = flip_image(Image.open(fnpath))
                texture.paste(fnimg, import_coords(x, y))
                print('Pasted texture ' + fn + ' into textures' + ' with coords ' + str(x) + ', ' + str(y))
                x += 1
                if x == 4:
                    y += 1
                    x = 0
            if files < 0:
                break
        if files < 0:
            break
    texture = texture.transpose(Image.FLIP_TOP_BOTTOM)
    try:
        texture.save(TEXTURE_PATH)
        print('Successfully created texture.png')
    except:
        print('Failed to create texture.png! Maybe check if write-access has given?')
        time.sleep(1)
        sys.exit('Texture error')
