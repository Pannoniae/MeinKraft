import pyglet
from controller import GameController
from images import image_process
from myio.load import GameLoader
from myio.save import GameSaver


VERSION = "0.5.3"


def main():


    image_process()
    ctrl = GameController(width=1920, height=1080, caption='My own cute Pyglet v%s' % VERSION,
                          resizable=True, vsync=True, fullscreen=True)
    # ctrl.log_events()
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
