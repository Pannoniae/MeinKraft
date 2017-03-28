from ..label import Label


class Console(Label):

    def __init__(self, master, msg, x, y, font_name="Arial", font_size=18, anchor_x="left", anchor_y="top",
                 color=(0, 0, 0, 255)):

        super().__init__(msg, x, y, font_name=font_name, font_size=font_size, anchor_x=anchor_x, anchor_y=anchor_y,
                            color=color)
        self.content = []
        from ..controller import GameController
        assert isinstance(master, GameController)
        self.master = master

    def show(self):
        """
        Draws the command console onto the screen.

        """
        msg = ''.join(self.content)
        # print(self.split())
        self.set_text(msg)

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

    def split(self):
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
        print(self.split())
        self.master.executer.execute_command(self.split()[0], self.split()[1])
        # clear buffer
        self.clear()
        # unset typing
        self.master.is_typing = False



