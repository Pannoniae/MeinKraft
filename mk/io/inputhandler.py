import pyglet
from pyglet.window import key, mouse




class InputHandler(object):

    def __init__(self, master):
        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

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
        if symbol == key.ESCAPE:
            self.master.set_exclusive_mouse(False)
        if not self.master.is_typing:
            if symbol == key.W:
                self.master.player.move_forward()
            elif symbol == key.S:
                self.master.player.move_backward()
            elif symbol == key.A:
                self.master.player.move_left()
            elif symbol == key.D:
                self.master.player.move_right()
            elif symbol == key.SPACE:
                self.master.player.jump()
            elif symbol == key.TAB:
                self.master.player.toggle_flying()
            elif symbol in self.master.num_keys:
                self.master.change_player_block(symbol)
            elif symbol == key.Z:
                self.master.zoom_state = 'in'

        elif symbol == key.BACKSPACE:
            self.master.console.del_char(1)
        elif symbol == key.ENTER:
            self.master.console.execute()


    def on_text(self, text):
        """ Called when the player types into the console.
        """
        if self.master.is_typing:
            if text != 'T':
                self.master.console.add_char(text)
                print("console content: %s" % self.master.console.read())
            else:
                print("console mode ended")
                self.master.is_typing = False
        elif text == 't':
            print("console mode entered")
            self.master.player.halt()
            self.master.is_typing = True
        self.master.console.show()

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
        if not self.master.is_typing:
            if symbol == key.W:
                self.master.player.move_backward()
            elif symbol == key.S:
                self.master.player.move_forward()
            elif symbol == key.A:
                self.master.player.move_right()
            elif symbol == key.D:
                self.master.player.move_left()
            elif symbol == key.SPACE:
                self.master.player.jumping = False
            elif symbol == key.Z:
                self.master.zoom_state = 'out'

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
        if self.master.exclusive:
            vector = self.master.player.get_sight_vector()
            block, previous = self.master.model.hit_test(self.master.player.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous:
                    self.master.model.add_block(previous, self.master.player.block)
                else:
                    self.master.bullet.fire(self.master.player.position)

            elif button == pyglet.window.mouse.LEFT and block:
                self.master.mine_block(block)
        else:
            self.master.set_exclusive_mouse(True)

        # the world has changed for the player
        self.master.world_changed()

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
        if self.master.exclusive:
            self.master.player.move(x, y, dx, dy)

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.master.label.y = height - 10
        x, y = self.master.width / 2, self.master.height / 2
        # construct reticle
        self.master.reticle.create(x, y)