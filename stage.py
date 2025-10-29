from pico2d import load_image

class Object:
    def __init__(self, w, h, x, y, image_file, id): # id 0이면 위만 충돌체크, 1이면 전체 충돌체크
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.image = load_image(image_file)
        self.id = id

class Stage:
    def __init__(self, id, w, h):
        self.id = id
        self.bg = None
        self.w, self.h = w, h

    def enter(self):  # 스테이지 시작 시 초기화
        if self.id == 0:
            self.bg = load_image("BG_0stage.png")
        elif self.id == 1:
            self.bg = load_image("BG_1stage.png")
        elif self.id == 2:
            self.bg = load_image("BG_2stage.png")
        elif self.id == 3:
            self.bg = load_image("BG_3stage.png")

    def exit(self):   # 스테이시 종료 시 처리
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

        player.x = 400
        player.y = 50

class Stage1(Stage):
    def __init__(self, w, h, player):
        super().__init__(1, w, h)
        self.bg = load_image("BG_1stage.png")
        if player:
            player.x, player.y = 40, 40
        self.floor_y = [10, 155, 290, 435]
        self.floors = []
        for idx, y in enumerate(self.floor_y):
            floor = Object(800, 50, w // 2, y, "floor_stage1.png", 0)
            self.floors.append(floor)


    def draw(self):
        super().draw()
        for floor in self.floors:
            floor.image.draw(floor.x, floor.y)

class Stage2(Stage):
    def __init__(self, w, h):
        super().__init__(2, w, h)

class Stage3(Stage):
    def __init__(self, w, h):
        super().__init__(3, w, h)