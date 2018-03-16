from gui.label import Label
from lang.executer import Executer

class Console(Label):

    def __init__(self, master, msg, x, y, font_name="Arial", font_size=18, anchor_x="left", anchor_y="top",
                 color=(0, 0, 0, 255)):

        super().__init__(msg, x, y, font_name=font_name, font_size=font_size, anchor_x=anchor_x, anchor_y=anchor_y,
                            color=color)
        self.content = []
        from controller import GameController
        assert isinstance(master, GameController)
        self.master = master
        self.command_executor = Executer(self.master)

    def read(self):
        """
        read out content of console
        non-destructive
        """
        return ''.join(self.content)

    def show(self):
        """
        Show the content of the command console on the screen.
        """
        self.set_text(self.read())

    def add_char(self, char):
        self.content.append(char)

    def del_char(self, num):
        if self.content:
            for i in range(num):
                del self.content[-1]

    def clear(self):
        """
        Clears console buffer.

        """
        self.content = []

    def parse(self):
        """ Split the command, and the arguments.

        Returns a tuple of the command, and another for args. """

        # if empty, return False, instead of crashing
        if not self.content:
            return False
        command = ''.join(self.content).split(' ')

        # return first element, then the rest
        return [command[0], (command[1:])]

    def execute(self):
        #execute command by the language parser
        print(self.parse())
        command, command_args = self.parse()
        try:
            cmd = self.command_executor.find_command(command)
            cmd.exec(command_args)
        except KeyError:
            print("command wasn't found")
        # clear buffer
        self.clear()
        # unset typing
        self.master.is_typing = False