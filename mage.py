from pico2d import load_image

from event import right_down, left_down, jump_down, right_up, left_up, jump_up, up_down, up_up, down_down, down_up
from state import Idle, Run, Jump, Up, Down
from state_machine import StateMachine

class Mage:
    def __init__(self, x=40, y=40):
        self.x = x
        self.y = y
        self.image = load_image("mage_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 31, 62]
        self.frame = 0

        self.dir = 0   # 가는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.can_up = False  # 위쪽으로 갈 수 있는지 여부

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.UP = Up(self)
        self.DOWN = Down(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {down_down: self.DOWN, up_down: self.UP, jump_down: self.JUMP, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN: {right_down: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, right_up: self.IDLE},
                self.JUMP: {jump_up: self.IDLE, right_down: self.RUN, left_down: self.RUN},
                self.DOWN: {down_up: self.IDLE},
                self.UP: {up_up: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_events(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트 전달

    def at_stage0_exit(self, x_target=900, y_target=80, eps=6):
        return abs(self.x - x_target) <= eps