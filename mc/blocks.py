# define MC block

from .geometry import tex_coords

class Block(object):
    """"represents a block

    TODO:  extends as needed
    """
    @classmethod
    def get_block_type(self):
        klassname = self.__name__
        return  klassname

    @classmethod
    def get_texture(self):
        # abstract
        raise NotImplemented

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

# safe for import from *
__all__ = [v.__name__ for k,v in globals().items() if hasattr(v, "get_texture") ]
