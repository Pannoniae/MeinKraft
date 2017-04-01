import shelve

from ..controller import GameController
from ..render.geometry import sectorize

DATASTORE = "laststate"

class GameLoader(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master

    def load_game(self):
        self.load_world()
        self.load_player()

    def load_world(self):
        try:
            with shelve.open(DATASTORE) as db:
                self.master.model.world = db['world']
                self.master.model.sectors = db['sectors']
                self.master.model.show_all_sectors()
        except KeyError:
            print("first launch, or save is corrupted?")
        print("world loaded")
        print(self.master.model.sectors.keys())

    def load_player(self):

        try:
            with shelve.open(DATASTORE) as db:
                status = db['player']
        except KeyError:
            print("first launch, or save is corrupted?")
        else:
            player = self.master.player
            player.flying = status["flying"]
            player.jumping = status["jumping"]
            player.position = status["position"]
            player.strafe = status["strafe"]
            player.rotation = status["rotation"]
            player.sector = status["sector"]
            player.block = status["block"]
            player.dy = status["dy"]
            self.master.model.show_sector(player.sector)
            self.master.player.update_sector()
            print("last player status loaded")


if __name__ == "__main__":
    ctrl = GameController(width=800, height=600, caption='Test', resizable=True, vsync=True)
    gameloader = GameLoader(ctrl)
    gameloader.load_game()
