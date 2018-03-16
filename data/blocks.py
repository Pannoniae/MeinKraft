# define MC blocks

from render.geometry import tex_coords, tex_coords_single, cube_vertices


class Block(object):
    """represents a block

    no block id's
    now the class itself is stored in the world storage


    TODO:  extend as needed
    """
    # save memory, not needed
    __slots__ = ["state"]

    def __init__(self):
        # test variable, it sets texture.

        # this is the length of list holds the textures used by the block
        self.state = 1

    texture_states = []

    # Whether player collides with this block.
    collision = True

    """
    Transparency works in a quite awkward way yet. If you define this variable to true, the block will be transparent.
    Else if the block doesn't collide, it will be transparent.
    """
    transparent = False


    # Sadly I cannot make this a property, it don't work. But, to conserve memory, it is called on the class, not the instance.
    @classmethod
    def is_transparent(cls):
        return True if cls.collision is False or cls.transparent else False

    def set_random_texture(self, idx):
        self.state = idx

    def get_texture(self):
        return tex_coords(*self.texture_states[self.state - 1])

    @classmethod
    def get_block_type(self):
        classname = self.__name__
        return classname


    @classmethod
    def get_vertices(cls, x, y, z):
        return cube_vertices(x, y, z, 0.5)

    @property
    def random_textures(self):
        return len(self.texture_states)


class BRICK(Block):
    # brick, stone
    texture_states = [((0, 0), (0, 0), (0, 0)), ((1, 0), (1, 0), (1, 0))]

class BRICK_SLAB(Block):

    #
    texture_states = [((0, 0), (0, 0), (1, 2))]

    transparent = True

    @classmethod
    def get_vertices(cls, x, y, z):
        return cube_vertices(x, y, z, 0.5, 0)


class DIRT(Block):

    texture_states =[((0, 2), (0, 2), (0, 2))]


class STONE(Block):

    texture_states = [((1, 0), (1, 0), (1, 0))]


class PATH(Block):

    texture_states = [((2, 1), (2, 0), (1, 1))]

    # It is transparent in some regard.
    transparent = True

    @classmethod
    def get_vertices(cls, x, y, z):
        # this is not filled completely, the upper 16th is transparent!
        return cube_vertices(x, y, z, 0.5, 7)


class GRASS(Block):

    texture_states = [((0, 1), (2, 0), (3, 0))]


class TALL_GRASS(Block):

    texture_states = [((2, 2))]

    collision = False

    @classmethod
    def get_vertices(cls, x, y, z):
        return cube_vertices(x, y, z, 0.5, mode="x")

    def get_texture(self):
        return tex_coords_single(self.texture_states[0])


class SAND(Block):

    texture_states = [((3, 1), (3, 1), (3, 1))]

    collision = False


class LOG(Block):

    texture_states = [((0, 2), (0, 2), (0, 2))]
