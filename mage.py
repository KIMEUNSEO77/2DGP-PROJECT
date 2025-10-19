from pico2d import load_image

from state_machine import StateMachine


class Idle:   # 가만히 서 있는 상태
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.player.frame = 0

    def draw(self):
        if self.player.face_dir == 1:   # 오른쪽 바라볼 때
            self.player.image.clip_draw(self.player.frames[self.player.frame], 0, 32, 40, self.player.x, 90)
        else:   # 왼쪽 바라볼 때
            self.player.image.clip_draw(self.player.frames[self.player.frame], 0, 32, 40,
                                         self.player.x, 90, -40, 32)
class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Jump:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Mage:
    def __init__(self, x=40, y=300):
        self.x = x
        self.y = y
        self.image = load_image("mage_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 33, 66]
        self.frame = 0

        self.dir = 0   # 가는 방향 (
        self.face_dir = 1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(

        )

    def update(self):
        self.x += 1
        self.frame = (self.frame + 1) % 3
    def draw(self):
        if self.image:
            self.image.clip_draw(self.frames[self.frame], 0, 32, 40, self.x, 90)
