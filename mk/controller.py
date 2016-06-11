# MC view
from __future__ import absolute_import
# third party imports
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
# project module imports
from .constants import *
from .blocks import STONE
from .model import Model
from .player import Player
from .reticle import Reticle
from .label import Label

from .bullet import Bullet
from .geometry import cube_vertices


class ZoomController(object):
    """
    control functionality specific to zooming
    """

    def __init__(self, *args, **kwargs):

        super(ZoomController, self).__init__(*args, **kwargs)
        # The FOV of the camera, used when zooming. Cannot be lower than 20.
        self.FOV = MAX_FOV

        # Variable holding the current zoom phase.
        self.zoom_state = None

        pyglet.clock.schedule_interval(self.check_zoom, 1.0 / TICKS_PER_SEC)


    def zoom_in_out(self, zoom):
        self.FOV -= zoom

    def check_zoom(self, dt):
        """ Runs the zooming script every tick. Used by pyglet to ensure steady tick rate and avoiding using time.sleep()
        Also, it's a bit clunky, so an explanation:

        There's a few zoom states.
        'in' means zooming in, 'out' is zooming out. When they're completed, state switches to 'yes' or 'no', accordingly.
        'toggle' is a special, when it's triggered, it immediately switches to an another state. This is here to prevent
        creating a getter function.

        """
        if self.zoom_state == 'in':
            if self.FOV != MIN_FOV:
                self.FOV -= 6
                self.reticle.transparency -= 0.1
            if self.FOV == MIN_FOV:
                self.zoom_state = 'yes'
        if self.zoom_state == 'out':
            if self.FOV != MAX_FOV:
                self.FOV += 6
                self.reticle.transparency += 0.1
            if self.FOV == MAX_FOV:
                self.zoom_state = 'no'
        if self.zoom_state == 'no':
            self.FOV = MAX_FOV
        if self.zoom_state == 'yes':
            self.FOV = MIN_FOV
        if self.zoom_state == 'toggle':
            if self.FOV == MIN_FOV:
                self.zoom_state = 'out'
            if self.FOV == MAX_FOV:
                self.zoom_state = 'in'
            else:
                print(
                'Error when determining zoom state. Did you try to zoom in zoom mode or are you debugging the code?')


    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.Z:
            self.zoom_state = 'in'


    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.Z:
            self.zoom_state = 'out'


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """ Called when the player scrolls the mouse. Used for zooming.
        """
        self.zoom_in_out(scroll_y)



class GameController(ZoomController, pyglet.window.Window):

    # Convenience list of num keys.
    num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]


    def __init__(self, *args, **kwargs):

        super(GameController, self).__init__(*args, **kwargs)

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
        self.bullet = Bullet(self)

        # The label that is displayed in the top left of the canvas.
        self.label = Label("", x=10, y=self.height - 10)

        # The label that is displayed in the bottom left of the canvas.
        self.label_bottom = Label("", x=10, y=10, anchor_y='bottom')


        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.

        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        pyglet.clock.schedule_interval(self.update_game, 1.0 / GAME_TICKS_PER_SEC)

        self.bullet.test()

        self.vector = self.player.get_sight_vector()
        self.target_block = self.model.hit_test(self.player.position, self.vector)[0]


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
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.model.process_queue()

        self.player.update(dt)
        self.player_changed_world()



    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """
        if self.exclusive:
            vector = self.player.get_sight_vector()
            block, previous = self.model.hit_test(self.player.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                self.build_block(previous)
            elif button == pyglet.window.mouse.LEFT and block:
                self.mine_block(block)
        else:
            self.set_exclusive_mouse(True)

        # the world has changed for the player
        self.world_changed()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if self.exclusive:
            self.player.move(x,y, dx, dy)



    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.player.move_forward()
        elif symbol == key.S:
            self.player.move_backward()
        elif symbol == key.A:
            self.player.move_left()
        elif symbol == key.D:
            self.player.move_right()
        elif symbol == key.SPACE:
            self.player.jump()
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.player.toggle_flying()
        elif symbol in self.num_keys:
            self.change_player_block(symbol)

        ZoomController.on_key_press(self, symbol, modifiers)


    def change_player_block(self, key_symbol):
        index = (key_symbol - self.num_keys[0]) % len(self.player.inventory)
        self.player.change_active_block(index)

    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.player.move_backward()
        elif symbol == key.S:
            self.player.move_forward()
        elif symbol == key.A:
            self.player.move_right()
        elif symbol == key.D:
            self.player.move_left()
        elif symbol == key.SPACE:
            self.player.jumping = False

        ZoomController.on_key_release(self, symbol, modifiers)

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        x, y = self.width / 2, self.height / 2
        # construct reticle
        self.reticle.create(x, y)


    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

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
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.FOV, width / float(height), 0.1, 60.0)
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
        """ Called by pyglet to draw the canvas.
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
        self.reticle.draw()

    def update_game(self, dt):
        """ Update game tick which is slower than update() for performance reasons.

        """
        self.prep_focused_block()
        self.draw_label()
        self.draw_bottom_label()

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
            glLineStipple(1, 0x17AF)
            glEnable(GL_LINE_STIPPLE)
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()

    def mine_block(self, block):
        """
        mine targeted block
        :return:
        """
        texture = self.model.world[block]
        if texture != STONE:
            self.model.remove_block(block)

    def build_block(self, block):
        """
        add new block
        :param block:
        :return:
        """
        if block:
            self.model.add_block(block, self.player.block)
        else:
            self.zoom_state = 'toggle'


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
            msg = '%s block, zoom %s, flying=%s' % (block.get_block_type(), self.zoom_state, self.player.flying)
            self.label_bottom.set_text(msg)


    def setup(self):
        from .gl_setup import setup
        setup()
