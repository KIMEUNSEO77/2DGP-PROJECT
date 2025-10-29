from pico2d import load_image

from event import right_down, left_down, jump_down, right_up, left_up, jump_up, up_down, up_up, down_down, down_up
from state import Idle, Run, Jump, Up, Down
from state_machine import StateMachine

class Player:
    def __init__(self, x=40, y=40, id=0):
        self.x = x
        self.y = y
        if id == 0:
            self.image = load_image("mage_sprite.png")
        elif id == 1:
            self.image = load_image("knight_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 31, 62]
        self.frame = 0

        self.dir = 0   # 가는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.prev_x, self.prev_y = self.x, self.y   # 이전 위치 저장
        self.w, self.h = 32, 40

        self.gravity = -5
        self.on_ground = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        # self.UP = Up(self)
        # self.DOWN = Down(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {jump_down: self.JUMP, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, right_up: self.IDLE},
                self.JUMP: {jump_up: self.IDLE, right_down: self.RUN, left_down: self.RUN}
            }
        )

    def aabb(self):
        hw, hh = self.w * 0.5, self.h * 0.5
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def update(self):
        self.state_machine.update()
        self.prev_x, self.prev_y = self.x, self.y

        self.on_ground = False # 매 프레임마다 땅에 있는지 초기화

        if not self.on_ground:
            self.y += self.gravity

        if self.x >= 990:
            self.x = 990
        elif self.x <= 20:
            self.x = 20


    def draw(self):
        self.state_machine.draw()

    def handle_events(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트 전달

    def at_stage0_exit(self, x_target=920, eps=6):
        return abs(self.x - x_target) <= eps