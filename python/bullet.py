from __future__ import absolute_import
from .view import Window

class Bullet(Window):
    def __init__(self, *args, **kwargs):

        super(Window, self).__init__(*args, **kwargs)

        # The velocity of the bullet in the x, y, z directions.
        self.velocity = (0, 0, 0)

        # How much damage does it deal.
        self.damage = 50

        # Position in game world.
        self.position = (0, 0, 0)

        # If is has landed, it deals damage.
        self.landed = False

        self.window = super(Bullet, self).__init__(*args, **kwargs)

    def test(self):
        print(self.window.position)