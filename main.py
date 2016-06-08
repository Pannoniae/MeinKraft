from __future__ import absolute_import

import pyglet

from python.images import image_process
from python.view import Window

# from profilehooks import profile

VERSION = "0.4"


# @profile
def main():
    image_process()
    window = Window(width=800, height=600, caption='My own cute Pyglet v%s' % VERSION, resizable=True, vsync=False)
    # window.logevents()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    window.setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()
