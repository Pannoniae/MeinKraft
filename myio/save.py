import shelve

from config import DATASTORE
from controller import GameController


class GameSaver(object):

    def __init__(self, master):
        self.master: GameController = master

    def save_game(self):
        self.save_world()
        self.save_player()

    def save_world(self):
        with shelve.open(DATASTORE) as db:
            db['world'] = self.master.model.world
            db['sectors'] = self.master.model.sectors
            db['sector'] = self.master.player.sector
        print("world saved")

    def save_player(self):
        player = self.master.player
        status = dict(
                        flying=player.flying,
                        jumping=player.jumping,
                        position=player.position,
                        strafe=player.strafe,
                        rotation=player.rotation,
                        block=player.block,
                        dy=player.velocity[1])
        with shelve.open(DATASTORE) as db:
            db['player'] = status
        print("player saved")