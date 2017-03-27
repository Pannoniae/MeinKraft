
import pyglet

class Label(pyglet.text.Label):
    " display some info on screen"

    def __init__(self, msg, x=0, y=0, font_name="Arial", font_size=18, anchor_x="left", anchor_y="top", color=(0,0,0,255)):

        super().__init__(msg, font_name=font_name, font_size=font_size,
                                       x=x, y=y, anchor_x=anchor_x, anchor_y=anchor_y,
                                       color=color)

    def set_position(self, x=None, y=None):
        if x:
            self.x = x
        if y:
            self.y = y

    def set_text(self, text):
        self.text = text
        self.draw()
