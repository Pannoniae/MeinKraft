import shelve

from mk.controller import GameController

DATASTORE = "laststate"

class GameSaver(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master


    def save_game(self):
        self.save_world()
        self.save_player()

    def save_world(self):
        model = self.master.model
        with shelve.open(DATASTORE) as db:
            db['world'] = model.world
        self.master.debug("world saved")

    def save_player(self):
        player = self.master.player
        status = dict(flying=player.flying,
                      jumping=player.jumping,
                      position=player.position,
                      strafe=player.strafe,
                      rotation=player.rotation,
                      sector=player.sector,
                      block=player.block,
                      dy=player.dy)
        with shelve.open(DATASTORE) as db:
            db['player'] = status
        self.master.debug("player saved")


if __name__ == "__main__":
    ctrl = GameController(width=800, height=600, caption='Test', resizable=True, vsync=True)
    gamesaver = GameSaver(ctrl)
    gamesaver.save_game()
