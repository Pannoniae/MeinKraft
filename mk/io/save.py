from ..controller import GameController


class GameSaver(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master

    def save_game(self):
        self.save_world()
        self.save_player()

    def save_world(self):
        pass

    def save_player(self):
        pass
