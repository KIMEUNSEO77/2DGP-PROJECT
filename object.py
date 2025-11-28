# object.py
from pico2d import load_image, draw_rectangle, load_wav
import game_framework
import game_world
import hint_mode
import game_clear_mode
import game_over_mode

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
            game_world.remove_object(self)

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
        self.sfx = load_wav("sound/sound_object.wav")
        self.sfx.set_volume(128)

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
            self.sfx.play()

            if self.key:
                self.finded = True
            elif self.hint_index is not None:   # 힌트 책일 경우
                hint_mode.hint_index = self.hint_index
                game_world.remove_object(self)
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
            game_world.remove_object(self)
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
            game_world.remove_object(self)
        if group == 'attack:monster':
            try:
                game_world.remove_collision_object(self)
            except:
                pass

            # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
            try:
                game_world.remove_object(self)
            except:
                pass

class Box():
    def __init__(self, x, y, key=False, hint_index=0, poison_1=False, poison_2=False):
        self.x = x
        self.y = y
        self.image = load_image("object_box.png")
        self.w, self.h = 50, 35
        self.key = key
        self.finded = False
        self.key_image = load_image("key_image.png")

        self.hint_index = hint_index
        self.poison_1 = poison_1
        self.poison_2 = poison_2

        self.sfx = load_wav("sound/sound_object.wav")
        self.sfx.set_volume(128)

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
            self.sfx.play()

            if self.key:
                self.finded = True
                # game_world.remove_object(self)
            elif self.hint_index is not None and other.hintOpened == False:   # 힌트 박스일 경우
                other.hintOpened = True
                hint_mode.hint_index = self.hint_index
                game_framework.push_mode(hint_mode)

                # 1) 충돌 그룹에서 먼저 무조건 제거
                try:
                    game_world.remove_collision_object(self)
                except:
                    pass

                # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
                try:
                    game_world.remove_object(self)
                except:
                    pass
            elif self.poison_1:
                other.poison_1 = True
                try:
                    game_world.remove_collision_object(self)
                except:
                    pass

                # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
                try:
                    game_world.remove_object(self)
                except:
                    pass
            elif self.poison_2:
                other.poison_2 = True
                game_world.remove_object(self)
            else:
                try:
                    game_world.remove_collision_object(self)
                except:
                    pass

                # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
                try:
                    game_world.remove_object(self)
                except:
                    pass

# 마녀의 생명줄 (3스테이지)
class LifeLine():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y

        self.id = id   # 0이면 빨강, 1이면 초록, 2이면 보라(진짜)
        if self.id == 0:
            self.image = load_image("lifeline_red.png")
        elif self.id == 1:
            self.image = load_image("lifeline_green.png")
        elif self.id == 2:
            self.image = load_image("lifeline_purple.png")

        self.w, self.h = 80, 400

        self.hp = 100.0   # 생명줄 체력 (공격 받으면 감소함)
        self.hp_image = load_image("lifeline_hp.png")

        self.afx = load_wav("sound/sound_lifeline.wav")
        self.afx.set_volume(128)

    def draw(self):
        self.image.clip_composite_draw(0, 0, 181, 811,
                                           0, '', self.x, self.y, self.w, self.h)
        # 체력바 그리기
        # 체력 비율에 따라 hp바 가로 길이 조절
        hp_ratio = max(0.0, min(self.hp, 100.0)) / 100.0
        if hp_ratio > 0.0:
            src_full_w = 877  # 원본 이미지의 전체 가로 픽셀
            src_w = max(1, int(src_full_w * hp_ratio))  # 소스에서 잘라낼 너비
            draw_w = max(1, int(self.w * hp_ratio))  # 화면에 그릴 너비
            # 왼쪽 기준으로 줄어들게 하기 위해 중심 보정
            draw_x = self.x - (self.w - draw_w) / 2.0

            self.hp_image.clip_composite_draw(0, 0, src_w, 93,
                                              0, '', draw_x, self.y - 50, draw_w, 15)

        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 32, self.y-200, self.x + 32, self.y-50

    def handle_collision(self, group, other):
        if group == 'attack:monster':
            self.afx.play()

            self.hp -= 10.0
            if self.hp <= 0:
                if self.id == 2:
                    game_framework.change_mode(game_clear_mode)
                else:
                    game_framework.change_mode(game_over_mode)
                try:
                    game_world.remove_collision_object(self)
                except:
                    pass

                # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
                try:
                    game_world.remove_object(self)
                except:
                    pass


# 3스테이지 인형 몬스터들
class MonsterDoll_1():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage3_1.png")
        self.w, self.h = 32, 40

        self.frames = [0, 28, 56]
        self.frame = 0
        self.frame_idx = 0

    def draw(self):
        self.frame_idx = int(self.frame)
        self.image.clip_composite_draw(self.frames[self.frame_idx], 0, 28, 38,
                                           0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += BOOK_SPEED_PPS * 2.0 * game_framework.frame_time

    def get_bb(self):
        return self.x - 16, self.y - 20, self.x + 16, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:monster' and other.god_mode == False:
            game_world.remove_object(self)
        if group == 'attack:monster':
            try:
                game_world.remove_collision_object(self)
            except:
                pass

            # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
            try:
                game_world.remove_object(self)
            except:
                pass

class MonsterDoll_2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage3_2.png")
        self.w, self.h = 32, 40

        self.frames = [0, 28, 56]
        self.frame = 0
        self.frame_idx = 0

    def draw(self):
        self.frame_idx = int(self.frame)
        self.image.clip_composite_draw(self.frames[self.frame_idx], 0, 28, 38,
                                           0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x -= BOOK_SPEED_PPS * 0.5 * game_framework.frame_time

    def get_bb(self):
        return self.x - 16, self.y - 20, self.x + 16, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:monster' and other.god_mode == False:
            game_world.remove_object(self)
        if group == 'attack:monster':
            try:
                game_world.remove_collision_object(self)
            except:
                pass

            # 2) 월드에서 제거 (이미 빠졌을 수도 있으니 예외 무시)
            try:
                game_world.remove_object(self)
            except:
                pass

class MonsterDoll_3():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("monster_stage3_3.png")
        self.w, self.h = 35, 55
        # 처음에는 생명줄 앞에 가만히 서있음(공격받으면 움직이기 시작함)
        self.active = False   # 활성화 여부

        self.frames_x = [0, 30, 60]
        self.frames_y = [0, 49, 97, 145]

        self.frame = 0
        self.frame_idx_x = 0
        self.frame_idx_y = 0

        self.dir_x = -1   # x축 이동 방향
        self.dir_y = 0

    def draw(self):
        self.frame_idx_x = int(self.frame)
        if not self.active:
            self.image.clip_composite_draw(self.frames_x[1], self.frames_y[3], 30, 49,
                                            0, '', self.x, self.y, self.w, self.h)
        else:
            self.image.clip_composite_draw(self.frames_x[self.frame_idx_x], self.frames_y[self.frame_idx_y], 30, 49,
                                            0, '', self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.active:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.x += self.dir_x * BOOK_SPEED_PPS * game_framework.frame_time
            self.y += self.dir_y * BOOK_SPEED_PPS * game_framework.frame_time

        if self.x <= 15:
            self.x = 16
            self.dir_x = 0
            self.dir_y = -1
            self.frame_idx_y = 3
        elif self.y <= 60:
            self.y = 61
            self.dir_x = 1
            self.dir_y = 0
            self.frame_idx_y = 1
        elif self.x >= 985:
            self.x = 984
            self.dir_x = 0
            self.dir_y = 1
            self.frame_idx_y = 0
        elif self.y >= 300:
            self.y = 299
            self.dir_x = -1
            self.dir_y = 0
            self.frame_idx_y = 2

    def get_bb(self):
        return self.x - 16, self.y - 20, self.x + 16, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:monster' and other.god_mode == False:
            game_world.remove_object(self)

        if group == 'attack:monster':
            if self.active == False:
                self.active = True   # 공격받으면 활성화되어 움직이기 시작함
            else:
                # 분열: 자기 제거 후 두 개 생성하고 충돌 등록까지 수행
                left = MonsterDoll_3(400, 300)
                right = MonsterDoll_3(460, 300)

                left.active = True
                right.active = True

                # 서로 반대 또는 원래 방향으로 퍼지게 설정 (원하면 반대로)
                left.dir_x = -1
                left.dir_y = 0
                right.dir_x = -1
                right.dir_y = 0

                # 상태 복사
                left.frame = self.frame
                right.frame = self.frame
                left.frame_idx_y = self.frame_idx_y
                right.frame_idx_y = self.frame_idx_y

                # 월드와 충돌 시스템에 등록
                try:
                    game_world.add_object(left)
                    game_world.add_object(right)
                except Exception:
                    pass

                # 충돌 처리에 등록하는 API가 있는 경우 호출 (실패해도 무시)
                try:
                    game_world.add_collision_pairs("player:monster", None, left)
                    game_world.add_collision_pairs("attack:monster", None, left)
                    game_world.add_collision_pairs("player:monster", None, right)
                    game_world.add_collision_pairs("attack:monster", None, right)
                except Exception:
                    pass

                # 원본 충돌 등록 해제 및 월드에서 제거
                try:
                    game_world.remove_collision_object(self)
                except Exception:
                    pass
                try:
                    game_world.remove_object(self)
                except Exception:
                    pass
