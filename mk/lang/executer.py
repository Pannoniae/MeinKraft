from ..controller import GameController


class CommandExecuter(object):

    def __init__(self, master):
        assert isinstance(master, GameController)
        self.master = master

    def execute_command(self, command, *args):
        pass