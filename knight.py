from pico2d import load_image


class Knight:
    def __init__(self, x=40, y=300):
        self.x = x
        self.y = y
        self.image = load_image("knight_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 31, 62]
        self.frame = 0

    def update(self):
        self.x += 1
        self.frame = (self.frame + 1) % 3
    def draw(self):
        if self.image:
            self.image.clip_draw(self.frames[self.frame], 0, 28, 38, self.x, 90)
