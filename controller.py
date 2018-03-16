# controller classes

from __future__ import absolute_import

# third party imports
import pyglet
from pyglet.gl import *
from pyglet.window import key

# project module imports
from render.renderer import Renderer
from myio.console import Console
from myio.inputhandler import InputHandler
from render.zoomer import Zoomer
from config import *
from data.blocks import *
from model import Model
from player import Player
from render.reticle import Reticle
from gui.label import Label



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

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # The crosshairs at the center of the screen.
        self.reticle = Reticle(1.0)

        # Instance of the model that handles the world.
        self.model = Model()

        # Instance of Player object
        self.player = Player(self.model)


        # The label that is displayed in the top left of the canvas.
        self.label = Label(x=20, y=self.height - 20)

        # The label that is displayed in the bottom left of the canvas.
        self.label_bottom = Label(x=20, y=20)

        # The command console where you can input things.
        self.console = Console(self, "", 100, 100)

        # Whether you are typing in the console, or not.
        self.is_typing = False

        self.FOV = MAX_FOV

        self.zoomer = Zoomer(self)

        self.input = InputHandler(self)

        self.renderer = Renderer(self)

        self.schedule_updates()

        self.vector = self.player.get_sight_vector()
        self.target_block = self.model.hit_test(self.player.position, self.vector)[0]

        self.fps_display = pyglet.clock.ClockDisplay()
        self.reticle.create(self.width / 2, self.height / 2)

        self.prev_pos = 0, 0, 0


    def schedule_updates(self):
        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        #pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        pyglet.clock.schedule_interval(self.update_game, 1.0 / GAME_TICKS_PER_SEC)
        pyglet.clock.schedule_interval(self.speed, 1.0)


    def log_events(self):
        self.push_handlers(pyglet.window.event.WindowEventLogger())

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super().set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def update(self):
        """ This method is scheduled to be called repeatedly by the pyglet clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        while not self.has_exit: # never, controller doesn't have has_exit property
            dt = pyglet.clock.tick()
            self.player.update(dt)
            # update stuff
            self.reticle.shift =  10
            self.reticle.create(self.width / 2, self.height / 2)
            self.prev_pos = self.player.position

            self.draw()
            self.dispatch_events()



    def update_game(self, dt):
        """
        This method is scheduled to be called repeatedly by the pyglet clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        Update game tick which is slower than update() for performance reasons.
        """
        self.prepare_focused_block()

        self.model.process_queue()


    def speed(self, dt):
        pass


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

    def draw(self):
        """ Pass drawing to the renderer. """
        self.renderer.on_draw()
        self.flip()

    def get_targeted_block(self):
        self.vector = self.player.get_sight_vector()
        position = self.model.hit_test(self.player.position, self.vector)[0]
        return self.model.get_block(position)

    def get_targeted_position(self):
        self.vector = self.player.get_sight_vector()
        position = self.model.hit_test(self.player.position, self.vector)[0]
        return position


    def prepare_focused_block(self):
        """ Computes focused block target in game tick to speed up game.

        """
        self.vector = self.player.get_sight_vector()
        self.target_block = self.model.hit_test(self.player.position, self.vector)[0]

    def mine_block(self, block_position):
        """
        mine targeted block
        """
        block = self.model.world[block_position]
        if type(block) != STONE:
            self.model.remove_block(block_position)

    def build_block(self, block_position):
        """

        Deprecated method, use model.add_block.

        Add a new block at this position. Use the current block in the player's inventory.
        """
        self.model.add_block(block_position, self.player.block)

