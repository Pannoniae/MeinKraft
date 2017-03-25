import os.path
import hashlib

from .config import BLOCKDATA_FOLDER


def imgpath(filename):

    """ Returns the path for that image. """

    return os.path.join(os.path.dirname(os.path.dirname(__file__)), BLOCKDATA_FOLDER, filename)


def base_path(filename):

    """ Returns the game folder """

    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

def get_block_id(filename):

    """ Returns the number from the end of filename. """

    return filename.split('_')[-1]

def md5_file(file):

    """ md5 function for files.

        Takes a file argument, outputs a string. """

    try:
        file = open(file, 'rb')
        stream = file.read()
        return md5(stream)

    except IOError:
        return 0

def md5(data):

    """ md5 function for string. """

    md5_lib = hashlib.md5()
    md5_lib.update(data)
    return md5_lib.hexdigest()
