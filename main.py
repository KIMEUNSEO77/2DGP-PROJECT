from pico2d import *

from mage import Mage

WIDTH, HEIGHT = 1000, 600
player = 1  # 0: mage, 1: knight

class Knight:
    def __init__(self, x=40, y=300):
        self.x = x
        self.y = y
        self.image = load_image("knight_sprite.png")
        # (x, y) 좌표를 담는 프레임 리스트
        self.frames = [0, 33, 66]
        self.frame = 0

    def update(self):
        self.x += 1
        self.frame = (self.frame + 1) % 3
    def draw(self):
        if self.image:
            self.image.clip_draw(self.frames[self.frame], 0, 32, 40, self.x, 90)


class Stage:
    def __init__(self, id):
        self.id = id
        self.bg = None

    def enter(self):  # 스테이지 시작 시 초기화
        if self.id == 0:
            self.bg = load_image("Tutorial_BG.png")

    def exit(self):   # 스테이시 종료 시 처리
        self.bg = None
 
    def update(self): # 게임 로직 업데이트
        pass

    def draw(self): # 화면 그리기
        if self.bg:
            self.bg.draw(WIDTH // 2, HEIGHT // 2)

    def handle_events(self, event):
        pass

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

def reset_world():
    global running
    running = True

    global world   # 모든 객체를 담을 수 있는 리스트
    world = []

    stage = Stage(0)
    stage.enter()
    world.append(stage)
    if player == 0:
        mage = Mage()
        world.append(mage)
    else:
        knight = Knight()
        world.append(knight)

def update_world():   # 객체들의 상호작용, 행위 업데이트
    for obj in world:
        obj.update()

def render_world():   # 객체들 그리기
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()

running = True

# game loop
reset_world()

while running:
    handle_events()
    # close_canvas()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
