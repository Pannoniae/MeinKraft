# controller classes

import logging

# third party imports
import pyglet
from pyglet.gl import *
from pyglet.window import key

# project module imports
from .io.console import Console
from .io.inputhandler import InputHandler
from .render.zoomer import Zoomer
from .config import *
from .blocks import *
from .model import Model
from .player import Player
from .render.reticle import Reticle
from .label import Label
from .bullet import Bullet
from .render.geometry import cube_vertices



class GameController(pyglet.window.Window):

    """
     input and output handler, game controller class
    """

    # Convenience list of num keys
    num_keys = [
        key._1, key._2, key._3, key._4, key._5,
        key._6, key._7, key._8, key._9, key._0]

    def __init__(self, *args, **kwargs):

        super(GameController, self).__init__(*args, **kwargs)

        # initialize logging
        self.init_logger()

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # The crosshairs at the center of the screen.
        self.reticle = Reticle(1.0)

        # Instance of the model that handles the world.
        self.model = Model()

        # Instance of Player object
        self.player = Player()
        self.world_changed()

        # Instance of the bullet physics that handles the weapons.
        self.bullet = Bullet()

        # The label that is displayed in the top left of the canvas.
        self.label = Label("", x=10, y=self.height - 10)

        # The label that is displayed in the bottom left of the canvas.
        self.label_bottom = Label("", x=10, y=10, anchor_y='bottom')

        # The command console where you can input things.
        self.console = Console(self, "", 10, 9, anchor_x='left', anchor_y='top')

        # Whether you are typing in the console, or not.
        self.is_typing = False

        self.FOV = MAX_FOV

        self.zoomer = Zoomer(self)

        self.input = InputHandler(self)

        self.schedule_updates()

        self.vector = self.player.get_sight_vector()
        self.target_block = self.model.hit_test(self.player.position, self.vector)[0]


    def init_logger(self):
        self.log = logging.getLogger("meinkraft")
        self.log.setLevel(logging.DEBUG)
        out_hdlr = logging.StreamHandler() # stdout
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        out_hdlr.setLevel(logging.DEBUG)
        self.log.addHandler(out_hdlr)

    def debug(self, msg, *args):
        self.log.debug(msg, *args)


    def schedule_updates(self):
        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        pyglet.clock.schedule_interval(self.update_game, 1.0 / GAME_TICKS_PER_SEC)
        pyglet.clock.schedule_interval(self.update_info, 1.0 / INFO_TICKS_PER_SEC)

    def world_changed(self):
        """
        notify the player that the world has changed
        """
        self.player.world_changed(self.model)

    def player_changed_world(self):
        """
        synchronize world info
        """
        self.model = self.player.model

    def logevents(self):
        self.push_handlers(pyglet.window.event.WindowEventLogger())

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(GameController, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.model.process_queue()

        self.player.update(dt)
        self.player_changed_world()
        self.bullet.update(self.player)


    def update_game(self, dt):
        """
        This method is scheduled to be called repeatedly by the pyglet clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        Update game tick which is slower than update() for performance reasons.
        """
        self.prep_focused_block()

    def update_info(self, dt):
        """
        This method is scheduled to be called repeatedly by the pyglet clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        Update info tick
            improve performance by displaying info less frequently
        """
        self.draw_label()
        self.draw_bottom_label()
        self.console.show()


    def change_player_block(self, key_symbol):
        index = (key_symbol - self.num_keys[0]) % len(self.player.inventory)
        self.player.change_active_block(index)


    # Bindings for input in input class. When keyboard or mouse is pressed, this section gives the InputHandler class the handling.

    def on_key_press(self, symbol, modifiers):
        self.input.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.input.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.input.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.input.on_mouse_press(x, y, button, modifiers)

    def on_resize(self, width, height):
        self.input.on_resize(width, height)

    def on_text(self, text):
        self.input.on_text(text)

    # Drawing.

    def set_2d(self):
        """ Configure OpenGL to show in 2d.

        """
        width, height = self.get_size()
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
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.zoomer.FOV, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)

    def get_targeted_block(self):
        self.vector = self.player.get_sight_vector()
        position = self.model.hit_test(self.player.position, self.vector)[0]
        return self.model.get_block(position)

    def on_draw(self):
        """ Called by pyglet to show the canvas.
        """
        self.clear()
        pyglet.clock.tick()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.get_targeted_block()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_bottom_label()
        self.reticle.show()


    def prep_focused_block(self):
        """ Computes focused block target in game tick to speed up game.

        """
        self.vector = self.player.get_sight_vector()
        self.target_block = self.model.hit_test(self.player.position, self.vector)[0]

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        if self.target_block:
            x, y, z = self.target_block
            glPushAttrib(GL_ENABLE_BIT)
            #glLineStipple(1, 0x17AF)
            #glEnable(GL_LINE_STIPPLE)
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()

    def mine_block(self, block_position):
        """
        mine targeted block
        :return:
        """
        texture = self.model.world[block_position]
        if texture != STONE:
            self.model.remove_block(block_position)

    def build_block(self, block_position):
        """
        Add a new block at this position. Use the current block in the player's inventory.
        :param block_position:  3-tuple of coordinates
        :return:
        """
        self.model.add_block(block_position, self.player.block)

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.player.position
        msg = '%02d/%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), pyglet.clock.get_fps_limit(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.set_text(msg)

    def draw_bottom_label(self):
        """ Draw the debug label in the bottom left of the screen.
    
        """
        block = self.get_targeted_block()
        if block:
            msg = '%s block, zoom %s, flying=%s' % (block.get_block_type(), self.zoomer.zoom_state, self.player.flying)
            self.label_bottom.set_text(msg)


    def setup(self):
        from mk.render.gl_setup import setup
        setup()



