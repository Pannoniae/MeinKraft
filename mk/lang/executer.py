class Executer(object):

    def __init__(self, master):
        self.master = master

    def execute_command(self, command, *args):
        print("executing %s " % command)
        pass