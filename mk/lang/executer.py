from ..utils import str2cls



class Executer(object):

    def __init__(self, master):
        self.master = master

    def find_command(self, command):
        return eval(Command.cmd_table[command])(self.master)



class Command(object):

    def __init__(self, master):
        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

    cmd_table = {
        "remove": "BlockRemoverCommand",
        "set_block": "BlockSetterCommand",
        "set_fov": "ZoomerCommand",
    }

class BlockRemoverCommand(Command):


    def __init__(self, master):
        super().__init__(master)
        from ..controller import GameController
        assert isinstance(master, GameController)

    def exec(self, args):
        target_block = self.master.get_targeted_block()
        from ..blocks import Block
        assert isinstance(target_block, Block)
        self.master.model.remove_block(self.master.get_targeted_pos())


    version = 1
    author = "Pannoniae"
    api_version = 1

class BlockSetterCommand(Command):
    pass


class ZoomerCommand(Command):
    pass




