import math

import pyglet
from pyglet.gl import *

from mk.render.geometry import cube_vertices


class Renderer(object):

    def __init__(self, master):
        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.master.player.position
        msg = '%02d/%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), pyglet.clock.get_fps_limit(), x, y, z,
            len(self.master.model._shown), len(self.master.model.world))
        self.master.label.set_text(msg)

    def draw_bottom_label(self):
        """ Draw the debug label in the bottom left of the screen.

        """
        block = self.master.get_targeted_block()
        if block:
            msg = '%s block, zoom %s, flying=%s' % (block.get_block_type(), self.master.zoomer.zoom_state, self.master.player.flying)
            self.master.label_bottom.set_text(msg)

    def setup(self):
        from mk.render.gl_setup import setup
        setup()

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        if self.master.target_block:
            x, y, z = self.master.target_block
            glPushAttrib(GL_ENABLE_BIT)
            # glLineStipple(1, 0x17AF)
            # glEnable(GL_LINE_STIPPLE)
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()

    def on_draw(self):
        """ Called by pyglet to show the canvas.
        """
        self.master.clear()
        #pyglet.clock.tick()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.master.model.batch.draw()
        self.master.get_targeted_block()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_bottom_label()
        self.master.reticle.show()
        self.master.console.show()

    def set_2d(self):
        """ Configure OpenGL to show in 2d.

        """
        width, height = self.master.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to show in 3d.

        """
        width, height = self.master.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.master.zoomer.FOV, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.master.player.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.master.player.position
        glTranslatef(-x, -y, -z)
