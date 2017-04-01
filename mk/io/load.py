import shelve

from mk.controller import GameController

DATASTORE = "laststate"

class GameLoader(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master

    def load_game(self):
        #self.load_world()
        #self.load_player()
        pass

    def load_world(self):
        model = self.master.model
        with shelve.open(DATASTORE) as db:
            model.world = db['world']
        print("world loaded")

    def load_player(self):

        with shelve.open(DATASTORE) as db:
            status = db['player']

        player = self.master.player
        player.flying = status["flying"]
        player.jumping = status["jumping"]
        player.position = status["position"]
        player.strafe = status["strafe"]
        player.rotation = status["rotation"]
        player.sector = status["sector"]
        player.block = status["block"]
        player.dy = status["dy"]
        print("last player status loaded")


if __name__ == "__main__":
    ctrl = GameController(width=800, height=600, caption='Test', resizable=True, vsync=True)
    gameloader = GameLoader(ctrl)
    gameloader.load_game()
