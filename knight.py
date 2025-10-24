from pico2d import load_image

from event import right_down, left_down, jump_down, right_up, left_up, up_down, down_down, up_up, down_up
from state import Idle, Run, Jump, Up, Down
from state_machine import StateMachine

class Knight:
    def __init__(self, x=40, y=80):
        self.x = x
        self.y = y
        self.image = load_image("knight_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 30, 61]
        self.frame = 0

        self.dir = 0  # 가는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = 1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.UP = Up(self)
        self.DOWN = Down(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {down_down: self.DOWN, up_down: self.UP, right_down: self.RUN, left_down: self.RUN,
                            right_up: self.RUN, left_up: self.RUN},
                self.RUN: {up_down: self.UP, down_down: self.DOWN, right_down: self.IDLE, left_down: self.IDLE,
                           left_up: self.IDLE, right_up: self.IDLE},
                self.UP: {right_down: self.RUN, down_down: self.DOWN, left_down: self.RUN, up_up: self.IDLE},
                self.DOWN: {right_down: self.RUN, down_down: self.DOWN, left_down: self.RUN, down_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_events(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트 전달

    def at_stage0_exit(self, x_target=900, y_target=80, eps=6):
        return abs(self.x - x_target) <= eps and abs(self.y - y_target) <= eps
