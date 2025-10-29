from pico2d import *

import game_world
from knight import Knight
from mage import Mage
from stage import Stage
from stage import Stage0
from stage import Stage1
from stage import Stage2
from stage import Stage3

WIDTH, HEIGHT = 1000, 600
player = 0 # 0: mage, 1: knight
cur_stage = 0 # 현재 스테이지 번호
cur_stage_obj = None # 현재 스테이지 객체


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if player == 1:
                knight.handle_events(event)
            else:
                mage.handle_events(event)

open_canvas(WIDTH, HEIGHT)

def change_stage(new_stage):
    global mage, cur_stage, knight, cur_stage_obj

    # 기존 월드 객체들 정리
    if cur_stage_obj is not None:
        game_world.remove_object(cur_stage_obj)
        cur_stage_obj = None
    cur_stage = new_stage

    if cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT)
    else:
        stage = Stage0(WIDTH, HEIGHT)
    stage.enter()
    game_world.add_object(stage, 0)
    cur_stage_obj = stage

    # 플레이어를 월드에 다시 추가하고 위치/방향/상태/이벤트 초기화
    stage_start_positions = {
        0: {0: (400, 50), 1: (400, 50)},  # 스테이지0의 mage(0), knight(1)
        1: {0: (40, 40), 1: (40, 40)},  # 스테이지1 시작 위치
        2: {0: (40, 140), 1: (40, 120)},  # 스테이지2 시작 위치
        3: {0: (900, 80), 1: (900, 60)},  # 스테이지3 시작 위치
    }
    sx, sy = stage_start_positions.get(cur_stage, stage_start_positions[0]).get(player, (50, 80))



def reset_world():   # 모든 객체 초기화
    global running, cur_stage, mage, knight, cur_stage_obj
    running = True

    # global world   # 모든 객체를 담을 수 있는 리스트
    if player == 0:
        mage = Mage()
        mage.vy = 0
        mage.on_ground = False

        stage = Stage0(mage, WIDTH, HEIGHT)
        game_world.add_object(stage, 0)
        game_world.add_object(mage, 1)
    else:
        knight = Knight()
        knight.vy = 0
        knight.on_ground = False

        stage = Stage0(knight, WIDTH, HEIGHT)
        game_world.add_object(stage, 0)
        game_world.add_object(knight, 1)

        # cur_stage = 0
    stage.enter()
    cur_stage_obj = stage

def update_world():   # 객체들의 상호작용, 행위 업데이트
    game_world.update()

def render_world():   # 객체들 그리기
    clear_canvas()
    game_world.render()
    update_canvas()

running = True

# game loop
reset_world()

while running:
    handle_events()

    player_obj = mage if player == 0 else knight

    update_world()

    if player == 0:
        if mage.at_stage0_exit():
            change_stage(1)
    if player == 1:
        if knight.at_stage0_exit():
            change_stage(1)

    render_world()
    delay(0.05)

close_canvas()
