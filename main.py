from __future__ import absolute_import

import pyglet
from mc.view import Window
from mc.images import image_process

VERSION = "0.2"

def main():
    # create texture.png
    image_process()

    window = Window(width=800, height=600, caption='My own cute Pyglet v%s' % VERSION, resizable=True)
    window.logevents()
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    window.setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
