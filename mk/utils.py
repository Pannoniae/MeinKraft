import hashlib
import os.path


def str2cls(module, string):
    """ Returns a class object from a class name. """
    return getattr(module, string)


def imgpath(filename):

    """ Returns the path for that image. """
    from .config import BLOCKDATA_FOLDER
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), BLOCKDATA_FOLDER, filename)


def base_path(filename):

    """ Returns the game folder """

    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)

def get_block_id(filename):

    """ Returns the number from the end of filename. """

    return int(filename.split('_')[-1].split('.')[0])

def md5_file(file):

    """ md5 function for files.

        Takes a file argument, outputs a string. """

    try:
        with open(file, 'rb') as file:
            stream = file.read()
        return md5(stream)
    except IOError:
        raise IOError("Opening file failed")

def md5(data):

    """ md5 function for string. """

    md5_lib = hashlib.md5()
    md5_lib.update(data)
    return md5_lib.hexdigest()
