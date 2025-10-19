from pico2d import *

from knight import Knight
from mage import Mage
from stage import Stage

WIDTH, HEIGHT = 1000, 600
player = 1  # 0: mage, 1: knight
cur_stage = 0


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas(WIDTH, HEIGHT)

def reset_world():
    global running, cur_stage
    running = True

    global world   # 모든 객체를 담을 수 있는 리스트
    world = []

    stage = Stage(cur_stage, WIDTH, HEIGHT)
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
