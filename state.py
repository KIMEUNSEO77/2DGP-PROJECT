from event import right_down, left_down, right_up, left_up, up_down, down_down, up_up, down_up
import game_framework

w, h = 32, 40

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
# RUN
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# JUMP
JUMP_SPEED_PPS = 750.0
GRAVITY_PPS = 1800.0
# Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

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
        global w, h
        if self.player.face_dir == 1:   # 오른쪽 바라볼 때
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)
        else:   # 왼쪽 바라볼 때
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, 'h', self.player.x, self.player.y, w * 1.5, h * 1.5)


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
        # self.player.frame = (self.player.frame + 1) % 3
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        self.player.frame_idx = int(self.player.frame)
        global w, h
        if self.player.face_dir == 1:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame_idx], 45, w, h,
                                                  0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)
        else:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame_idx], 45, w, h,
                                                  0, 'h', self.player.x, self.player.y, w * 1.5, h * 1.5)

class Jump:
    def __init__(self, player):
        self.player = player
        self.cur_y = 0.0  # y증가량
        self.dy = 0.0

    def enter(self, e):
        self.player.frame = 1
        self.dy = JUMP_SPEED_PPS
        self.cur_y = 0

    def exit(self, e):
        self.cur_y = 0
        self.dy = 0.0

    def do(self):
        if self.cur_y < 150:
            self.player.y += self.dy * game_framework.frame_time
            self.cur_y += self.dy * game_framework.frame_time

    def draw(self):
        global w, h
        if self.player.face_dir == 1:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)
        else:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, 'h', self.player.x, self.player.y, w * 1.5, h * 1.5)

class Up:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if up_down(e) or down_up(e):
            self.player.dir = 1

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 3
        self.player.y += self.player.dir * 5

    def draw(self):
        global w, h
        self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 0, w, h,
                                              0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)

class Down:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if down_down(e) or up_up(e):
            self.player.dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 3
        self.player.y += self.player.dir * 5

    def draw(self):
        global w, h
        self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 140, w, h,
                                              0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)