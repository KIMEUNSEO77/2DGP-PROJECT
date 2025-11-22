# stage.py
from pico2d import load_image

import game_world
from game_world import remove_collision_object
from object import Object, MonsterBook, Book, MonsterVet, MonsterSkull, Box, LifeLine, MonsterDoll_1, MonsterDoll_2
import random
import time


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
            game_world.add_collision_pairs("player:object", None, obj)

    def exit(self):  # 스테이지 종료 시 처리
        print("Stage", self.id, "exit")

        # 안전 제거 함수
        def safe_remove(obj):
            # 충돌 제거 시도 (없으면 조용히 패스)
            try:
                remove_collision_object(obj)
            except:
                pass
            # 월드에서 제거 시도 (없으면 조용히 패스)
            try:
                game_world.remove_object(obj)
            except:
                pass

        # floors 제거
        for obj in list(self.floors):
            safe_remove(obj)

        # monsters 제거
        for monster in list(self.monsters):
            safe_remove(monster)

        # objects 제거
        for obj in list(self.objects):
            safe_remove(obj)

        # 리스트 초기화
        self.floors.clear()
        self.monsters.clear()
        self.objects.clear()


        self.bg = None


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
        self.objects = []
        self.monsters = []
        self.floor = Object(1000, 10, w // 2, 10, "floor_stage0.png", 0)
        self.floors.append(self.floor)
        player.x = 400
        player.y = 600
        player.gravity = -10
    def enter(self):
        super().enter()
    def draw(self):
        super().draw()
    def exit(self):
        super().exit()
    def update(self):
        pass




class Stage1(Stage):
    def __init__(self, w, h, player):
        super().__init__(1, w, h)
        self.player = player
        self.bg = load_image("BG_1stage.png")
        if player:
            player.x, player.y = 60, 100
        self.floor_y = [10, 155, 295, 440]

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

        # key_index = random.randint(0, 17)
        key_index = 17   # key 인덱스를 17로 고정
        self.book_x = [200, 400, 600, 800, 100, 300, 500, 700, 900, 150, 350, 550, 750, 100, 300, 500, 700, 900]
        self.book_y = [80, 80, 80, 80, 210, 210, 210, 210, 210, 350, 350, 350, 350, 485, 485, 485, 485, 485]

        # 인덱스별 힌트 매핑 (요청한 매핑)
        hint_map = { 0: 1, 4: 2, 10: 3, 15: 4, 6: 5 }

        # key인 인덱스는 True
        for i, (bx, by) in enumerate(zip(self.book_x, self.book_y)):
            hint_idx = hint_map.get(i)  # 없으면 None
            book = Book(bx, by, random.randint(1, 5), key=(i == key_index), hint_index=hint_idx)
            self.objects.append(book)

    def enter(self):
        super().enter()

    def draw(self):
        super().draw()

    def exit(self):
        super().exit()

    def update(self):
        pass





class Stage2(Stage):
    def __init__(self, w, h, player):
        super().__init__(2, w, h)
        self.bg = load_image("BG_2stage.png")
        if player:
            player.x, player.y = 60, 500

        self.player = player

        self.floors = []
        self.monsters = []
        self.objects = []

        self.active = False  # 스테이지 활성화 상태

        floor = Object(1000, 10, w // 2, 20, "floor_stage2.png", 0)
        self.floors.append(floor)

        self.monster_y = [130, 260, 390, 520]
        self.monster_x = [900, 500, 100, 700]
        for mx, my in zip(self.monster_x, self.monster_y):
            monster = MonsterVet(mx, my, player.id)
            self.monsters.append(monster)

        self.platform_x = [50, 300, 550, 700, 950, 150, 400, 650, 900, 100, 300, 550, 750, 950, 200, 450, 700, 900,
                           50, 250, 500, 750, 900]
        self.platform_y = [100, 120, 140, 160, 140, 200, 220, 240, 260, 300, 320, 340, 360, 340, 400, 420, 440, 460,
                           500, 520, 540, 560, 540]
        for px, py in zip(self.platform_x, self.platform_y):
            platform = Object(100, 10, px, py, "floor_stage2_3.png", 0)
            self.floors.append(platform)

        #key_index = random.randint(0, 26)   # key인 인덱스는 True
        key_index = 4  # key 인덱스를 4로 고정
        self.box_x = [50, 300, 550, 700, 950, 150, 400, 650, 900, 100, 300, 550, 750, 950, 200, 450, 700, 900,
                           250, 500, 750, 900, 100, 300, 500, 800]
        self.box_y = [120, 140, 160, 180, 160, 220, 240, 260, 280, 320, 340, 360, 380, 360, 420, 440, 460, 480,
                            540, 560, 580, 560, 30, 30, 30, 30]

        # 인덱스별 힌트 매핑 (요청한 매핑)
        hint_map = {9: 6, 6: 7, 15: 8, 7: 9, 13: 10}
        poision_1_idx = [18, 19, 20, 21]
        poison_2_idx = [22, 23, 24, 25]

        for i, (bx, by) in enumerate(zip(self.box_x, self.box_y)):
            hint_idx = hint_map.get(i)  # 없으면 None
            # 생성자가 key 인자를 받는다면
            box = Box(bx, by, key=(i == key_index), hint_index=hint_idx, poison_1=(i in poision_1_idx), poison_2=(i in poison_2_idx))
            self.objects.append(box)

    def enter(self):
        super().enter()
        self._last_spawn = time.time()
        self._spawn_interval = 5.0  # 5초마다 스폰

        for monster in self.monsters:
            game_world.add_collision_pairs("attack:monster", None, monster)

        self.active = True  # 스테이지 활성화

    def draw(self):
        super().draw()

    def exit(self):
        super().exit()
        self.player.poison_1 = False
        self.player.poison_2 = False
        self.active = False  # 스테이지 비활성화

    def update(self):
        if not self.active:
            return

        now = time.time()
        if self._last_spawn is None:
            self._last_spawn = now

        # 5초마다 MonsterSkull 생성
        if now - self._last_spawn >= self._spawn_interval:
            # 스폰 위치: 오른쪽 화면(예시) 및 y는 랜덤 선택
            spawn_x = random.randint(100, 900)
            spawn_y = 600
            skull = MonsterSkull(spawn_x, spawn_y)

            # 월드와 스테이지 리스트에 추가, 충돌 등록
            self.monsters.append(skull)
            game_world.add_object(skull, 2)
            try:
                game_world.add_collision_pairs("player:monster", None, skull)
                game_world.add_collision_pairs("attack:monster", None, skull)
            except:
                pass

            self._last_spawn = now




class Stage3(Stage):
    def __init__(self, w, h, player):
        super().__init__(3, w, h)
        self.bg = load_image("BG_3stage.png")
        if player:
            player.x, player.y = 60, 500

        self.active = False  # 스테이지 활성화 상태

        self.floors = []
        self.monsters = []
        self.objects = []

        self.floor = Object(1000, 10, w // 2, 10, "floor_stage3.png", 0)
        self.floors.append(self.floor)

        self.life_line_red = LifeLine(200, 500, 0)
        self.monsters.append(self.life_line_red)
        self.life_line_green = LifeLine(500, 500, 1)
        self.monsters.append(self.life_line_green)
        self.life_line_purple = LifeLine(800, 500, 2)
        self.monsters.append(self.life_line_purple)

        # 테스트용
        #self.monster_1 = MonsterDoll_1(100, 70)
        #self.monsters.append(self.monster_1)

    def enter(self):
        super().enter()

        self._last_spawn = time.time()
        self._spawn_interval = 5.0  # 5초마다 스폰

        self._spawn_interval_2 = 3.0  # 3초마다 스폰

        self.active = True  # 스테이지 활성화
        for monster in self.monsters:
            game_world.add_collision_pairs("attack:monster", None, monster)

    def draw(self):
        super().draw()

    def exit(self):
        super().exit()

    def update(self):
        if not self.active:
            return

        now = time.time()
        if self._last_spawn is None:
            self._last_spawn = now

        # 5초마다 Monster1 생성
        if now - self._last_spawn >= self._spawn_interval:
            # 스폰 위치: 왼쪽 끝
            spawn_x = 0
            spawn_y = 60
            doll_1 = MonsterDoll_1(spawn_x, spawn_y)

            # 월드와 스테이지 리스트에 추가, 충돌 등록
            self.monsters.append(doll_1)
            game_world.add_object(doll_1, 2)
            try:
                game_world.add_collision_pairs("player:monster", None, doll_1)
                game_world.add_collision_pairs("attack:monster", None, doll_1)
            except:
                pass

            self._last_spawn = now


        # 3초마다 Monster2 생성
        if now - self._last_spawn >= self._spawn_interval_2:
            # 스폰 위치: 오른쪽 끝
            spawn_x = 1000
            spawn_y = 60
            doll_2 = MonsterDoll_2(spawn_x, spawn_y)

            # 월드와 스테이지 리스트에 추가, 충돌 등록
            self.monsters.append(doll_2)
            game_world.add_object(doll_2, 2)
            try:
                game_world.add_collision_pairs("player:monster", None, doll_2)
                game_world.add_collision_pairs("attack:monster", None, doll_2)
            except:
                pass

            self._last_spawn = now