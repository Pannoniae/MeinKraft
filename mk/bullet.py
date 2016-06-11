from __future__ import absolute_import

class Bullet(object):
    def __init__(self, game):

        self.game = game

        # The velocity of the bullet in the x, y, z directions.
        self.velocity = (0, 0, 0)

        # How much damage does it deal.
        self.damage = 50

        # Position in game world.
        self.position = (0, 0, 0)

        # If is has landed, it deals damage.
        self.landed = False


    def test(self):

        print("parent ", self.game.player.position)
        print("me ", self.position)