from pico2d import load_image
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Object:
    def __init__(self, w, h, x, y, image_file, id): # id 0이면 위만 충돌체크, 1이면 전체 충돌체크
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.image = load_image(image_file)
        self.id = id

    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass

    # 중심(x,y), 폭w, 높이h 기준 AABB
    def aabb(self):
        half_w, half_h = self.w * 0.5, self.h * 0.5
        left = self.x - half_w
        right = self.x + half_w
        bottom = self.y - half_h
        top = self.y + half_h
        return left, bottom, right, top

class MonsterBook():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage1.png")
        self.w, self.h = 32, 32
        self.dir = 1  # 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.frame = 0
        self.frames = [25, 180, 410, 635, 880]
        self.frame_idx = 0

    def draw(self):
        self.frame_idx = int(self.frame)
        if self.dir == 1:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 450, 200, 120,
                                                  0, '', self.x, self.y, self.w * 3, self.h * 3)
        else:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 450, self.w, self.h,
                                                  0, 'h', self.x, self.y, self.w, self.h)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

    def aabb(self):
        pass