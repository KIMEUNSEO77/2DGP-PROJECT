from pico2d import load_image

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

    def check_collision(self, player):
        """스테이지별로 오버라이드할 것. player는 x,y,w,h 같은 속성을 가정."""
        raise NotImplementedError

class Stage0(Stage):
    def __init__(self, player, w, h):
        super().__init__(0, w, h)
        player.x = 40
        player.y = 80

class Stage1(Stage):
    def __init__(self, player, w, h):
        super().__init__(1, w, h)
        player.x = 50
        player.y = 80

class Stage2(Stage):
    def __init__(self, w, h):
        super().__init__(2, w, h)

class Stage3(Stage):
    def __init__(self, w, h):
        super().__init__(3, w, h)