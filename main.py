from __future__ import absolute_import

import pyglet

from mk.controller import GameController
from mk.images import image_process

# from profilehooks import profile

VERSION = "0.4"


# @profile
def main():
    image_process()
    ctrl = GameController(width=800, height=600, caption='My own cute Pyglet v%s' % VERSION,
                            resizable=True, vsync=False)
    # ctrl.logevents()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    ctrl.set_exclusive_mouse(True)
    ctrl.setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()
