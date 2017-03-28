
# third party imports
import pyglet
from pyglet.gl import *


class Reticle(object):
    " The crosshairs at the center of the screen. "

    def __init__(self, transparency):

        # The reticle's transparency, it is transparent when scoping in.
        self.transparency = transparency
        self.vertexlist = None

        #How much it is shifted from the center.
        self.shift = 2.5


    def create(self, x, y):
        n = 10
        s = self.shift # a shift from the middle
        if self.vertexlist:
            self.vertexlist.delete()
        self.vertexlist = pyglet.graphics.vertex_list(8,
                                                      ('v2f',
                                                       (x - n, y, x - s, y, x + s, y, x + n, y, x, y - n, x, y - s, x,
                                                        y + s, x, y + n)
                                                       )
                                                      )

    def show(self):
        """ Draw the crosshairs in the center of the screen."""
        glColor4d(0, 0, 0, self.transparency)
        self.vertexlist.draw(GL_LINES)
