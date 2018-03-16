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


    def exec(self, args):
        target_block = self.master.get_targeted_block()
        from data.blocks import Block
        assert isinstance(target_block, Block)
        self.master.model.remove_block(self.master.get_targeted_pos())

    author = "Pannoniae"

class BlockSetterCommand(Command):
    def exec(self, args):
        print(args)
        target_block = self.master.get_targeted_block()
        from data.blocks import Block
        assert isinstance(target_block, Block)
        self.master.model.add_block(self.master.get_targeted_pos(), args[0])


class ZoomerCommand(Command):
    pass




