from pico2d import load_image


class Mage:
    def __init__(self, x=40, y=300):
        self.x = x
        self.y = y
        self.image = load_image("mage_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 33, 66]
        self.frame = 0

    def update(self):
        self.x += 1
        self.frame = (self.frame + 1) % 3
    def draw(self):
        if self.image:
            self.image.clip_draw(self.frames[self.frame], 0, 32, 40, self.x, 90)
