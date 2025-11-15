from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import hint_mode

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
# Book
BOOK_SPEED_KMPH = 10.0  # Km / Hour
BOOK_SPEED_MPM = (BOOK_SPEED_KMPH * 1000.0 / 60.0)
BOOK_SPEED_MPS = (BOOK_SPEED_MPM / 60.0)
BOOK_SPEED_PPS = (BOOK_SPEED_MPS * PIXEL_PER_METER)

# 사실상 바닥
class Object:
    def __init__(self, w, h, x, y, image_file, id): # id 0이면 위만 충돌체크, 1이면 전체 충돌체크
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.image = load_image(image_file)
        self.id = id

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        #draw_rectangle(*self.aabb())
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

# monster book 클래스 (1스테이지 몬스터)
class MonsterBook():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage1.png")
        self.w, self.h = 80, 50
        self.dir = 1  # 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.frame = 0
        self.frames = [25, 180, 410, 635, 880]
        self.frame_idx = 0

    def draw(self):
        self.frame_idx = int(self.frame)
        if self.dir == 1:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 450, 200, 120,
                                                  0, '', self.x, self.y, self.w, self.h)
        else:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 450, 200, 120,
                                                  0, 'h', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.x += self.dir * BOOK_SPEED_PPS * game_framework.frame_time
        if self.x >= 980:
            self.dir = -1
        elif self.x <= 20:
            self.dir = 1

    def get_bb(self):
        return self.x - 30, self.y - 20, self.x + 30, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:monster':
            print("Player collided with MonsterBook")

class Book():
    def __init__(self, x, y, image_type, key=False, hint_index=0):
        self.x = x
        self.y = y
        if image_type == 1:
            self.image = load_image("object_book_1.png")
        elif image_type == 2:
            self.image = load_image("object_book_2.png")
        elif image_type == 3:
            self.image = load_image("object_book_3.png")
        elif image_type == 4:
            self.image = load_image("object_book_4.png")
        elif image_type == 5:
            self.image = load_image("object_book_5.png")

        self.key = key
        self.key_image = load_image("key_image.png")
        self.w, self.h = 100, 100
        self.finded = False

        self.hint_index = hint_index

    def draw(self):
        self.image.clip_composite_draw(0, 0, 120, 120,
                                       0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

        if self.key and self.finded:
            self.key_image.clip_composite_draw(0, 0, 47, 111,
                                               0, '', 500, 300 + 40, 150, 300)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:object':
            if self.key:
                self.finded = True
                # game_world.remove_object(self)
            elif self.hint_index is not None:   # 힌트 책일 경우
                hint_mode.hint_index = self.hint_index
                game_framework.push_mode(hint_mode)
            else:
                game_world.remove_object(self)

class MonsterVet():
    def __init__(self, x, y, player_id):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage2.png")
        self.w, self.h = 80, 50
        self.dir = 1  # 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.frame = 0
        self.frames = [0, 130, 270, 410]
        self.frame_idx = 0
        self.player_id = player_id  # 플레이어 id에 따라서 충돌 효과 다름.
        self.speed_minus = 1.0   # 감속되는 스피드
        self.moving = True   # 이동 여부 (전사가 공격시 2초간 멈춤)
        self.freeze_time = 0.0 # 멈춘 시간

    def draw(self):
        self.frame_idx = int(self.frame)
        if self.dir == 1:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 0, 135, 85,
                                           0, '', self.x, self.y, self.w, self.h)
        else:
            self.image.clip_composite_draw(self.frames[self.frame_idx], 0, 135, 85,
                                           0, 'h', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.freeze_time > 0.0:
            self.freeze_time -= game_framework.frame_time
            if self.freeze_time <= 0.0:
                self.moving = True

        if self.moving:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.dir * BOOK_SPEED_PPS * game_framework.frame_time * self.speed_minus
        if self.x >= 980:
            self.dir = -1
        elif self.x <= 20:
            self.dir = 1

    def get_bb(self):
        return self.x - 30, self.y - 25, self.x + 30, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:monster':
            print("Player collided with MonsterVet")
        if group == 'attack:monster':
            if self.player_id == 0:
                self.speed_minus = max(0.1, self.speed_minus - 0.1)
            elif self.player_id == 1:
                self.moving = False
                self.freeze_time = 2.0  # 2초간 멈춤
            
class MonsterSkull():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage2_2.png")
        self.w, self.h = 80, 80

    def draw(self):
        self.image.clip_composite_draw(0, 0, 100, 100,
                                           0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.y -= 1.5 + BOOK_SPEED_PPS * game_framework.frame_time
        if self.y <= 30:
            self.y = 30

    def get_bb(self):
        return self.x - 30, self.y - 20, self.x + 30, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:monster':
            print("Player collided with MonsterSkull")
        if group == 'attack:monster':
            try:
                game_world.remove_object(self)
            except Exception as e:
                # 게임월드가 안전하게 처리한다면 이 블록은 실행되지 않음
                print("object.handle_collision: remove failed:", e)

class Box():
    def __init__(self, x, y, key=False):
        self.x = x
        self.y = y
        self.image = load_image("object_box.png")
        self.w, self.h = 50, 35
        self.key = key
        self.finded = False
        self.key_image = load_image("key_image.png")

    def draw(self):
        self.image.clip_composite_draw(0, 0, 175, 124,
                                           0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

        if self.key and self.finded:
            self.key_image.clip_composite_draw(0, 0, 47, 111,
                                               0, '', 500, 300 + 40, 150, 300)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 25, self.y - 17, self.x + 25, self.y + 17

    def handle_collision(self, group, other):
        if group == 'player:object':
            if self.key:
                self.finded = True
                # game_world.remove_object(self)
            else:
                game_world.remove_object(self)