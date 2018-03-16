from __future__ import absolute_import

class Bullet(object):
    def __init__(self):


        # The velocity of the bullet in the x, y, z directions.
        self.velocity = (0, 0, 0)

        # How much damage does it deal.
        self.damage = 50

        # Position in game world.
        self.position = (0, 0, 0)

        # If is has landed, it deals damage.
        self.landed = False

    def fire(self, position):
        """
        XXX: do something

        Parameters
        ----------
        position: tuple of len 3, position of the firing player.
        """
        self.position = position
        print(self.position)

    def update(self, player):
        """ Updates the bullet state with the player object.

        """
        dx, dy, dz = player.get_motion_vector()
        if dx < 0:
            dx -= 1
        else:
            dx += 1
        if dy < 0:
            dy -= 1
        else:
            dy += 1
        if dz < 0:
            dz -= 1
        else:
            dz += 1
        x, y, z = player.position

        self.position = x + dx, y + dy, z + dz