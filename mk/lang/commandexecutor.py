class CommandExecutor(object):

    def __init__(self, master):
        self.master = master

    def execute_command(self, command, *args):
        self.master.debug("executing %s " % command)
        pass