import hashlib
import os.path
import sys
import time

from PIL import Image

from .config import BLOCK_TEXTURE_SIZE, TEXTURE_PATH
from .utils import *








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
    texture = Image.new('RGBA', import_coords(4, 4), (0, 0, 0, 0))
    imgdir = sorted(os.listdir('blockdata'), key=get_block_id)
    files = len(imgdir)
    x = 0
    y = 0
    while x <= 4:
        while y <= 4:
            for fn in imgdir:
                fnpath = imgpath(fn)
                files -= 1
                if files < 0:
                    break
                fnimg = flip_image(Image.open(fnpath))
                texture.paste(fnimg, import_coords(x, y))
                print('Pasted texture ' + fn + " into textures with coords " + str(x) + ", " + str(y))
                x += 1
                if x == 4:
                    y += 1
                    x = 0
            if files < 0:
                break
        if files < 0:
            break
    texture = texture.transpose(Image.FLIP_TOP_BOTTOM)

    # Opening file

    try:
        hash = md5(texture)
    except:
        print('texture.png haven''t found! Creating a new one...')
    else:
        print('texture.png found! Checksum is: ' + hash)

    # Saving file

    try:
        texture.save(TEXTURE_PATH)
    except:
        print('Failed to create texture.png! Maybe check if write-access has given?')
        # Delay because it won't exit properly.
        time.sleep(1)
        sys.exit('Texture error')
    else:
        print('Successfully created texture.png')

    newhash = md5_file('texture.png')
    print('Checksum for new texture.png is: ' + newhash)
    #if oldhash == newhash:
    #    print('Checksums matched! Continuing program...')
    #else:
    #    print('Checksum mismatch! Generating new texture file...')
        # XXX Zsombor: ez a logika hibas. Itt semmi nem fogja ujra generalni a fajlt,

        # Ki kellene szamolni az ellenorzoosszeget, ezt eltarolni egy kulon fajlban, majd az abban levo ertekkel
        # kellene osszehasonlitani a kovetkezo programfutaskor a program altal talalt texture.png ellenorzoosszeget.
        # Ha nem egyeznek, akkor lekell generalni a texture.png-t, ha egyeznek, akkor meg nyilvan nem.
