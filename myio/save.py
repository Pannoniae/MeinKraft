import shelve

from controller import GameController

DATASTORE = "laststate"

class GameSaver(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master

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
                        dy=player.dy)
        with shelve.open(DATASTORE) as db:
            db['player'] = status
        print("player saved")