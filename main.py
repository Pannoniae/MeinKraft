from __future__ import absolute_import

import pyglet

from mk.controller import ZoomGameController
from mk.images import image_process

VERSION = "0.5"


def main():
    image_process()
    ctrl = ZoomGameController(width=800, height=600, caption='My own cute Pyglet v%s' % VERSION,
                          resizable=True, vsync=False)
    # ctrl.logevents()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    ctrl.set_exclusive_mouse(True)
    ctrl.setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()
