from pico2d import *
import random

class Mage:
    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y
        self.image = load_image("player_sprite.png")
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        if self.image:
            self.image.clip_draw(self.frame * 100, 140, 33, 40, self.x, 90)


class Knight:
    pass

class Stage:
    def __init__(self, id):
        self.id = id
        self.bg = None

    def enter(self):  # 스테이지 시작 시 초기화
        if self.id == 1:
            self.bg = load_image("Tutorial_BG.png")

    def exit(self):   # 스테이시 종료 시 처리
        self.bg = None
 
    def update(self): # 게임 로직 업데이트
        pass

    def draw(self): # 화면 그리기
        if self.bg:
            clear_canvas()
            self.bg.draw(400, 300)
            update_canvas()

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

    mage = Mage()
    world.append(mage)

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
    delay(0.02)

close_canvas()
