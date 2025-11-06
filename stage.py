from pico2d import load_image

import game_world
from object import Object, MonsterBook, Book
import random


class Stage:
    def __init__(self, id, w, h):
        self.id = id
        self.bg = None
        self.w, self.h = w, h

        self.floors = []    # 바닥 오브젝트 리스트
        self.monsters = []  # 몬스터 오브젝트 리스트
        self.objects = []   # 기타 오브젝트 리스트

        self._top_snap_tol = 8  # 위만 충돌 스냅 허용 오차(px)

    def check_collision(self, player):
        # 플레이어 상태 추출(없으면 폴백)
        vy = getattr(player, 'vy', 0.0)
        vx = getattr(player, 'vx', 0.0)
        prev_y = getattr(player, 'prev_y', player.y - vy * (1 / 60))  # 60fps 가정 폴백

        # on_ground 초기화
        if hasattr(player, 'on_ground'):
            player.on_ground = False

        # 플레이어 AABB
        pl, pb, pr, pt = player.aabb()

        for obj in self.floors:
            ol, ob, or_, ot = obj.aabb()

            # 빠른 탈락(AABB 안겹치면 continue)
            if pr <= ol or pl >= or_ or pt <= ob or pb >= ot:
                continue

            if obj.id == 0:
                # --- 위에서만 착지 ---
                self._resolve_top_only(player, ol, ob, or_, ot, vy, prev_y)
                # 착지/위치가 바뀌었을 수 있으니 AABB 갱신
                pl, pb, pr, pt = player.aabb()
            else:
                # --- 완전 솔리드 ---
                self._resolve_solid(player, pl, pb, pr, pt, ol, ob, or_, ot, vx, vy)
                # 위치가 바뀌었으니 AABB 갱신
                pl, pb, pr, pt = player.aabb()

    def _resolve_top_only(self, player, ol, ob, or_, ot, vy, prev_y):
        # 내려오는 중?
        descending = vy <= 0
        # 이전 프레임 발바닥 위치
        prev_foot = prev_y - (player.h * 0.5)
        # 위에서 접근했는지(스루 방지)
        coming_from_above = prev_foot >= ot - self._top_snap_tol

        # 수평 범위 겹침 체크(현 프레임)
        pl, pb, pr, pt = player.aabb()
        horiz_overlap = (pr > ol) and (pl < or_)

        if descending and coming_from_above and horiz_overlap:
            # 착지 스냅
            player.y = ot + (player.h * 0.5)
            if hasattr(player, 'vy'):
                player.vy = 0
            if hasattr(player, 'on_ground'):
                player.on_ground = True

    def _resolve_solid(self, player, pl, pb, pr, pt, ol, ob, or_, ot, vx, vy):
        # 침투량
        overlap_x = min(pr, or_) - max(pl, ol)
        overlap_y = min(pt, ot) - max(pb, ob)
        if overlap_x <= 0 or overlap_y <= 0:
            return

        # 최소 침투축으로 밀어내기
        if overlap_x < overlap_y:
            # X축으로 밀기
            center_obj = (ol + or_) * 0.5
            if player.x < center_obj:
                player.x -= overlap_x
            else:
                player.x += overlap_x
            if hasattr(player, 'vx'):
                player.vx = 0
        else:
            # Y축으로 밀기(천장/바닥)
            center_obj_y = (ob + ot) * 0.5
            if player.y < center_obj_y:
                # 아래에서 위로 박음 → 아래로
                player.y -= overlap_y
                if hasattr(player, 'vy') and vy > 0:
                    player.vy = 0
            else:
                # 위에서 내려옴 → 바닥에
                player.y += overlap_y
                if hasattr(player, 'vy'):
                    player.vy = 0
                if hasattr(player, 'on_ground'):
                    player.on_ground = True

    def enter(self):  # 스테이지 시작 시 초기화
        if self.id == 0:
            self.bg = load_image("BG_0stage.png")
        elif self.id == 1:
            self.bg = load_image("BG_1stage.png")
        elif self.id == 2:
            self.bg = load_image("BG_2stage.png")
        elif self.id == 3:
            self.bg = load_image("BG_3stage.png")

        for obj in self.floors:
            game_world.add_object(obj, 0)

        for monster in self.monsters:
            game_world.add_object(monster, 2)
            game_world.add_collision_pairs("player:monster", None, monster)

        for obj in self.objects:
            game_world.add_object(obj, 1)

    def exit(self):   # 스테이시 종료 시 처리
        self.bg = None
        for obj in list(self.floors):
            game_world.remove_object(obj)

    def update(self): # 게임 로직 업데이트
        pass

    def draw(self): # 화면 그리기
        if self.bg:
            self.bg.draw(self.w // 2, self.h // 2)

    def handle_events(self, event):
        pass

class Stage0(Stage):
    def __init__(self, player, w, h):
        super().__init__(0, w, h)
        self.floors = []
        self.floor = Object(1000, 10, w // 2, 10, "floor_stage0.png", 0)
        self.floors.append(self.floor)
        player.x = 400
        player.y = 600
        player.gravity = -10
    def enter(self):
        super().enter()
    def draw(self):
        super().draw()
    def update(self):
        pass

class Stage1(Stage):
    def __init__(self, w, h, player):
        super().__init__(1, w, h)
        self.bg = load_image("BG_1stage.png")
        if player:
            player.x, player.y = 60, 100
            player.gravity = -5
        self.floor_y = [30, 165, 300, 445]

        self.floors = []
        self.monsters = []
        self.objects = []

        for idx, y in enumerate(self.floor_y):
            floor = Object(1000, 10, w // 4, y, "floor_stage1.png", 0)
            self.floors.append(floor)

        self.monster_y = [220, 355, 500]
        self.monster_x = [900, 500, 100]
        for mx, my in zip(self.monster_x, self.monster_y):
            monster = MonsterBook(mx, my)
            self.monsters.append(monster)

        self.book_x = [200, 400, 600, 800, 100, 300, 500, 700, 900, 150, 350, 550, 750, 100, 300, 500, 700, 900]
        self.book_y = [80, 80, 80, 80, 180, 180, 180, 180, 180, 320, 320, 320, 320, 470, 470, 470, 470, 470]
        for bx, by in zip(self.book_x, self.book_y):
            book = Book(bx, by, random.randint(1, 5))
            self.objects.append(book)




    def enter(self):
        super().enter()

    def draw(self):
        super().draw()





class Stage2(Stage):
    def __init__(self, w, h):
        super().__init__(2, w, h)

class Stage3(Stage):
    def __init__(self, w, h):
        super().__init__(3, w, h)