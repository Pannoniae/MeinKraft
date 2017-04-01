import os.path

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
    """ Process the image files to texture.png at every program start.
    Yes, I know that this is a very ugly and slow loop, but no need to optimize, as it is called only once. """

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

    # Save texture internally

    try:
        texture.save(base_path('_texture.png'))
    except IOError:
        print("Couldn't save temponary texture file. Check write-access?")
    else:
        print("Saved temponary texture file from memory, checking md5 checksum...")

    # Compute hash texture in memory (that we created above)

    try:
        hash = md5_file(base_path('_texture.png'))
    except:
        print("Couldn't hash texture. md5 not installed?")
    else:
        print("Succesfully hashed texture in memory. Checksum is: " + hash)

    # Compute hash for old texture.png, if it exists

    try:
        newhash = md5_file('texture.png')
    except IOError:
        print("Couldn't open texture.png, check if it is properly saved, or maybe it isn't exists now?")
    else:
        print("Checksum for texture.png is: " + newhash)

    # Saving texture.png from memory
    if hash != newhash:
        try:
            texture.save(TEXTURE_PATH)
        except:
            print('Failed to create texture.png! Maybe check if write-access has given?')
            raise IOError("Failed to create texture map.")
        else:
            print("Successfully created texture.png, maybe it didn't exist or corrupted")
    else:
        print("All okay, cached textures will do the job, no need to resave.")
