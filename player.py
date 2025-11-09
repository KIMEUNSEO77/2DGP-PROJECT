from pico2d import load_image, draw_rectangle

from event import (right_down, left_down, jump_down, right_up, left_up, jump_up, up_down, up_up, down_down, down_up, right_attack_down, \
                   left_attack_down, up_attack_down, down_attack_down)
from state import Idle, Run, Jump, Up, Down
from state_machine import StateMachine
import game_framework
import game_world

GRAVITY_PPS = -200

class Player:
    def __init__(self, x=40, y=40, id=0):
        self.x = x
        self.y = y
        if id == 0:
            self.image = load_image("mage_sprite.png")
        elif id == 1:
            self.image = load_image("knight_sprite.png")
        self.id = id  # 0: mage, 1: knight
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 31, 62]
        self.frame = 0
        self.frame_idx = 0

        self.dir = 0   # 가는 방향 (1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.prev_x, self.prev_y = self.x, self.y   # 이전 위치 저장
        self.w, self.h = 32, 40

        self.on_ground = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        # self.UP = Up(self)
        # self.DOWN = Down(self)

        self.find_key = False


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {down_attack_down: self.IDLE, up_attack_down: self.IDLE, left_attack_down: self.IDLE, right_attack_down: self.IDLE,
                            jump_down: self.JUMP, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN: {left_attack_down: self.RUN, up_attack_down: self.RUN, down_attack_down: self.RUN, right_attack_down: self.RUN,
                           right_down: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, right_up: self.IDLE},
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
        
        # 점프 상태 아닐 때만 중력 적용
        if not self.on_ground and self.state_machine.cur_state != self.JUMP:
            self.y += GRAVITY_PPS * game_framework.frame_time

        if self.x >= 990:
            self.x = 990
        elif self.x <= 20:
            self.x = 20
        elif self.y >= 590:
            self.y = 590


    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_events(self, event):
        self.state_machine.handle_state_event(('INPUT', event))  # 스테이트 머신에 적합한 이벤트 전달

    def at_stage0_exit(self, x_target=920, eps=6):
        return abs(self.x - x_target) <= eps

    def get_bb(self):
        return self.x - 16, self.y - 20, self.x + 16, self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:monster':
            print("Player collided with monster!")

        elif group == 'player:object' and other.key:
            self.find_key = True

    def fire_ball_right(self):
        fire_ball = FireBall(self, self.x + 25, self.y, 1, 0)
        game_world.add_object(fire_ball, 1)
        game_world.add_collision_pairs("attack:monster", fire_ball, None)
    def fire_ball_left(self):
        fire_ball = FireBall(self, self.x - 25, self.y, -1, 0)
        game_world.add_object(fire_ball, 1)
        game_world.add_collision_pairs("attack:monster", fire_ball, None)
    def fire_ball_up(self):
        fire_ball = FireBall(self, self.x, self.y + 25, 0, 1)
        game_world.add_object(fire_ball, 1)
        game_world.add_collision_pairs("attack:monster", fire_ball, None)
    def fire_ball_down(self):
        fire_ball = FireBall(self, self.x, self.y - 25, 0, -1)
        game_world.add_object(fire_ball, 1)
        game_world.add_collision_pairs("attack:monster", fire_ball, None)

class FireBall:
    image = None
    def __init__(self, player, x, y, dirX, dirY):
        if FireBall.image is None and player.id == 0:
            FireBall.image = load_image("Mage_FireBall.png")
        elif FireBall.image is None and player.id == 1:
            FireBall.image = load_image("Knight_bullet.png")
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.w, self.h = 32, 32

        if player.id == 0:
            self.draw_w, self.draw_h = 60, 60
        elif player.id == 1:
            self.draw_w, self.draw_h = 16, 16

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.draw_w, self.draw_h,
                                       0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.dirX * 400 * game_framework.frame_time
        self.y += self.dirY * 400 * game_framework.frame_time

        if self.x > 1000 or self.x < 0 or self.y > 600 or self.y < 0:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            print("FireBall collided with monster!")
            try:
                game_world.remove_object(self)
            except Exception:
                pass