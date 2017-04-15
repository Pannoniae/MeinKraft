import pyglet

from mk.config import MAX_FOV, TICKS_PER_SEC, MIN_FOV, ZOOM_STATES


class Zoomer(object):
    """
    game controller which also allows zooming
    """

    def __init__(self, master):

        # The FOV of the camera, used when zooming. It cannot be lower than 20.
        self.FOV = MAX_FOV
        # Variable holding the current zoom phase.
        self.zoom_state = None
        # schedule zoom checking
        pyglet.clock.schedule_interval(self.check_zoom, 1.0 / TICKS_PER_SEC)

        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

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
        diff = MAX_FOV - MIN_FOV
        if self.zoom_state == 'in':
            if self.FOV != MIN_FOV:
                self.FOV -= diff / ZOOM_STATES
                self.master.reticle.transparency -= 1.0 / ZOOM_STATES
            if self.FOV == MIN_FOV:
                self.zoom_state = 'yes'
        if self.zoom_state == 'out':
            if self.FOV != MAX_FOV:
                self.FOV += diff / ZOOM_STATES
                self.master.reticle.transparency += 1.0 / ZOOM_STATES
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