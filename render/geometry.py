# geometry utility stuff

from config import SECTOR_SIZE

class MODE:

    mode_block = 0
    mode_x = 1


def cube_vertices(x, y, z, n, fill=8, mode=0):
    """
        Return the vertices of the cube at position x, y, z with size 2*n.

        fill: Can be between -8 and 8. -8 is an empty block, 8 is a full block, 0 is half a block.
        Exactly, (n = n/16 proportion of the block) fill = n - 8
        It should be noted that fill is computed at every pixel (1/16 block) but n is half a block, so we have to divide by 8.
    """
    from library import ffi, lib

    if mode == MODE.mode_block:
        array = ffi.new('float[72]')
        lib.cube_vertices(array, x, y, z, n, fill)
        return list(array)
    elif mode == MODE.mode_x:
        array = ffi.new('float[72]')
        lib.cube_vertices_x(array, x, y, z, n)
        return list(array)


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    #m = 1.0 / n
    #dx = x * m
    #dy = y * m
    #print([dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m])
    #return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m
    from library import ffi, lib

    array = ffi.new('float[8]')
    lib.tex_coord(array, x, y, n)
    return list(array)


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


def tex_coords_single(top):
    single = tex_coord(*top)
    result = []
    result.extend(single * 4)
    return result


FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return x, y, z


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.
    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return x, 0, z
