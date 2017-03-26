# define MC blocks

from mk.render.geometry import tex_coords, cube_vertices


class Block(object):
    """represents a block

    no block id's
    now the class itself is stored in the world storage


    TODO:  extends as needed
    """
    # save memory, not needed
    #__slots__ = ["get_texture", "get_block_type", "get_vertices"]

    @classmethod
    def get_texture(self):
        # abstract
        raise NotImplemented

    @classmethod
    def get_block_type(self):
        klassname = self.__name__
        return klassname

    @classmethod
    def get_vertices(self, x, y, z):
        return cube_vertices(x, y, z, 0.5)


class BRICK(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((0, 0), (0, 0), (0, 0))


class DIRT(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((0, 2), (0, 2), (0, 2))


class STONE(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((1, 0), (1, 0), (1, 0))


class PATH(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((2, 1), (2, 0), (1, 1))

    @classmethod
    def get_vertices(self, x, y, z):
        # this is not filled completely, the upper 16th is transparent!
        return cube_vertices(x, y, z, 0.5, 7)


class GRASS(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((0, 1), (2, 0), (3, 0))


class SAND(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((3, 1), (3, 1), (3, 1))


class LOG(Block):
    @classmethod
    def get_texture(self):
        return tex_coords((0, 2), (0, 2), (0, 2))


# safe for import from *
__all__ = [v.__name__ for k, v in globals().items() if hasattr(v, "get_texture")]
