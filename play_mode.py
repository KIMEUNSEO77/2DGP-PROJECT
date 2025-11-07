from pico2d import *

import game_world
from player import Player
from stage import Stage
from stage import Stage0
from stage import Stage1
from stage import Stage2
from stage import Stage3
import game_framework
import title_mode
import choose_mode
import first_to_second_mode

WIDTH, HEIGHT = 1000, 600
player = 0 # 0: mage, 1: knight
cur_stage = 0 # 현재 스테이지 번호 디버깅을 위해 1
cur_stage_obj = None # 현재 스테이지 객체
player_obj = None    # 현재 플레이어 객체

def handle_events():
    global player_obj

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(choose_mode)
        else:
            if player_obj is not None:
                player_obj.handle_events(event)

def change_stage(new_stage):
    global cur_stage, cur_stage_obj, player_obj

    # 기존 월드 객체들 정리
    if cur_stage_obj is not None:
        cur_stage_obj.exit()
        # game_world.remove_object(cur_stage_obj)
        cur_stage_obj = None
    cur_stage = new_stage

    if cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT, player_obj)
    else:
        stage = Stage0(WIDTH, HEIGHT)
    stage.enter()
    game_world.add_object(stage, 0)
    cur_stage_obj = stage


def init():   # 모든 객체 초기화
    global cur_stage, cur_stage_obj, player_obj

    # global world   # 모든 객체를 담을 수 있는 리스트
    if player == 0:
        player_obj = Player(40, 40, 0)
    else:
        player_obj = Player(40, 40, 1)
    player_obj.vy = 0
    stage = Stage0(player_obj, WIDTH, HEIGHT)
    game_world.add_object(stage, 0)
    game_world.add_object(player_obj, 1)
    game_world.add_collision_pairs('player:monster', player_obj, None)
    game_world.add_collision_pairs('player:object', player_obj, None)

    stage.enter()
    cur_stage_obj = stage

def update():   # 객체들의 상호작용, 행위 업데이트
    game_world.update()
    cur_stage_obj.check_collision(player_obj)

    if cur_stage == 0 and player_obj.at_stage0_exit():
        change_stage(1)

    if cur_stage == 1 and player_obj.find_key:
        delay(1.5)  # 열쇠 찾고 나서 잠시 대기
        game_framework.change_mode(first_to_second_mode)
        change_stage(2)

    game_world.handle_collisions()

def draw():   # 객체들 그리기
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():   # 게임 종료 시 처리
    game_world.clear()

