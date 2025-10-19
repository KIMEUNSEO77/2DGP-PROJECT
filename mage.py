from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d

from state_machine import StateMachine

# 이벤트 체크 함수
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def jump_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


class Idle:   # 가만히 서 있는 상태
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.player.frame = 1

    def draw(self):
        if self.player.face_dir == 1:   # 오른쪽 바라볼 때
            self.player.image.clip_draw(self.player.frames[self.player.frame], 0, 32, 40, self.player.x, self.player.y)
        else:   # 왼쪽 바라볼 때
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 0, 32, 40,
                                                  0, 'h', self.player.x, self.player.y, 32, 40)
class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.player.dir = self.player.face_dir = 1
        elif left_down(e) or right_up(e):
            self.player.dir = self.player.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 3
        self.player.x += self.player.dir * 5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frames[self.player.frame], 0, 32, 40, self.player.x, self.player.y)
        else:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 0, 32, 40,
                                                  0, 'h', self.player.x, self.player.y, 32, 40)

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
        self.frames = [0, 31, 62]
        self.frame = 0

        self.dir = 0   # 가는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN, jump_down: self.JUMP},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, right_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_events(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트 전달
