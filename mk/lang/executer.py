class CommandExecuter(object):

    def __init__(self, master):
        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

    def execute_command(self, command, *args):
        pass