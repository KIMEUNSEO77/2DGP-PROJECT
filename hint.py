from pico2d import load_image

class Hint:
    def __init__(self, hint_index=None):
        self.hint_index = hint_index
        if self.hint_index == 1:
            self.image = load_image("hint_stage1_1.png")
        elif self.hint_index == 2:
            self.image = load_image("hint_stage1_2.png")
        elif self.hint_index == 3:
            self.image = load_image("hint_stage1_3.png")
        elif self.hint_index == 4:
            self.image = load_image("hint_stage1_4.png")
        elif self.hint_index == 5:
            self.image = load_image("hint_stage1_5.png")

        else:
            pass

    def draw(self):
        self.image.draw(500, 300, 500, 300)

    def update(self):
        pass