import hashlib
import os.path
import sys
import time

from PIL import Image

from .constants import BLOCK_TEXTURE_SIZE


def imgpath(filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "blockdata", filename)

def texture_path(filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

TEXTURE_PATH = texture_path('texture.png')

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
    imgdir = sorted(os.listdir('blockdata'))
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
                print('Pasted texture ' + fn +  " into textures with coords " + str(x) + " " + str(y))
                x += 1
                if x == 4:
                    y += 1
                    x = 0
            if files < 0:
                break
        if files < 0:
            break
    texture = texture.transpose(Image.FLIP_TOP_BOTTOM)
    # Checksum computation
    if os.path.exists (TEXTURE_PATH):
        oldpng = open ('texture.png', 'rb')
        md5hash = oldpng.read ()
        hasher = hashlib.md5 ()
        hasher.update (md5hash)
        oldhash = hasher.hexdigest ()
        print('texture.png found! Checksum is: ', oldhash)
    else:
        print('texture.png haven''t found! Creating a new one...')
    try:
        texture.save(TEXTURE_PATH)
        print('Successfully created texture.png')
    except:
        print('Failed to create texture.png! Maybe check if write-access has given?')
        time.sleep(1)
        sys.exit('Texture error')
    if os.path.exists (TEXTURE_PATH):
        newpng = open ('texture.png', 'rb')
        md5hash = newpng.read ()
        hasher = hashlib.md5 ()
        hasher.update (md5hash)
        newhash = hasher.hexdigest ()
        print('Checksum for new texture.png is: ', newhash)
    if oldhash == newhash:
        print('Checksums matched! Continuing program...')
    else:
        print('Checksum mismatch! Generating new texture file...')
