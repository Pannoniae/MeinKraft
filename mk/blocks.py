# define MC blocks

from .render.geometry import tex_coords, cube_vertices


class Block(object):
    """represents a block

    no block id's
    now the class itself is stored in the world storage


    TODO:  extend as needed
    """
    # save memory, not needed
    #__slots__ = ["get_texture", "get_block_type", "get_vertices"]


    def __init__(self):
        # test variable, it sets texture.

        # this is the length of list holds the textures used by the block
        self.state = 1


    texture_states = []

    def set_random_texture(self, idx):
        self.state = idx

    def get_texture(self):
        return tex_coords(*self.texture_states[self.state - 1])

    @classmethod
    def get_block_type(self):
        klassname = self.__name__
        return klassname

    @classmethod
    def get_vertices(self, x, y, z):
        return cube_vertices(x, y, z, 0.5)

    @property
    def random_textures(self):
        return len(self.texture_states)



    # Whether player collides with this block.
    collision = True




class BRICK(Block):
    # brick, stone
    texture_states = [((0, 0), (0, 0), (0, 0)), ((1, 0), (1, 0), (1, 0))]

class BRICK_SLAB(Block):

    #
    texture_states = [((0, 0), (0, 0), (1, 2))]

    @classmethod
    def get_vertices(cls, x, y, z):
        return cube_vertices(x, y, z, 0.5, 0)


class DIRT(Block):

    texture_states =[((0, 2), (0, 2), (0, 2))]


class STONE(Block):

    texture_states = [((1, 0), (1, 0), (1, 0))]


class PATH(Block):

    texture_states = [((2, 1), (2, 0), (1, 1))]

    @classmethod
    def get_vertices(cls, x, y, z):
        # this is not filled completely, the upper 16th is transparent!
        return cube_vertices(x, y, z, 0.5, 7)


class GRASS(Block):

    texture_states = [((0, 1), (2, 0), (3, 0))]


class SAND(Block):

    texture_states = [((3, 1), (3, 1), (3, 1))]

    collision = False


class LOG(Block):

    texture_states = [((0, 2), (0, 2), (0, 2))]


# safe for import from *
#__all__ = [v.__name__ for k, v in globals().items() if hasattr(v, "get_texture")]
