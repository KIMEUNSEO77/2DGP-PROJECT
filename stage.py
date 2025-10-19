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
