# define MC blocks

from .geometry import tex_coords, cube_vertices

class Block(object):
    """"represents a block

    no block id's
    now the class itself is stored in the world storage


    TODO:  extends as needed
    """
    # save memory
    __slots__ = ["get_texture", "block_type", "get_vertices"]

    @classmethod
    def get_texture(self):
        # abstract
        raise NotImplemented

    @property
    def block_type(self):
        klassname = self.__name__
        return  klassname

    @classmethod
    def get_vertices(self, x, y, z):
        return cube_vertices(x, y, z, 0.5)


class GRASS(Block):

    @classmethod
    def get_texture(self):
        return tex_coords((1, 0), (0, 1), (0, 0))

class SAND(Block):

    @classmethod
    def get_texture(self):
        return tex_coords((1, 1), (1, 1), (1, 1))

class BRICK(Block):

    @classmethod
    def get_texture(self):
        return tex_coords((2, 0), (2, 0), (2, 0))

class STONE(Block):

    @classmethod
    def get_texture(self):
        return tex_coords((2, 1), (2, 1), (2, 1))

class DIRT(Block):

    @classmethod
    def get_texture(self):
        return tex_coords((0, 1), (0, 1), (0, 1))

class PATH(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((1, 2), (0, 1), (0, 2))

    @classmethod
    def get_vertices(self, x, y, z):
        # this is not filled completely!
        return cube_vertices(x, y, z, 0.5, 8)



# safe for import from *
__all__ = [v.__name__ for k,v in globals().items() if hasattr(v, "get_texture") ]
