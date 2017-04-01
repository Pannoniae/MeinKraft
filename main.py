import pyglet

from mk.controller import GameController
from mk.images import image_process

from mk.io.save import GameSaver
from mk.io.load import GameLoader

VERSION = "0.5.3"


def main():
    image_process()
    ctrl = GameController(width=800, height=600, caption='My own cute Pyglet v%s' % VERSION,
                          resizable=True, vsync=True)
    # ctrl.logevents()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    ctrl.set_exclusive_mouse(True)
    ctrl.renderer.setup()
    print("App started.")
    GameLoader(ctrl).load_game()
    pyglet.app.run()
    print("App stopped.")
    GameSaver(ctrl).save_game()


if __name__ == '__main__':
    main()
