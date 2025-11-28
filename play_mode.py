# play_mode.py
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
import second_to_third_mode
import game_over_mode

WIDTH, HEIGHT = 1000, 600
player = 0 # 0: mage, 1: knight
cur_stage = 0 # 현재 스테이지 번호 디버깅을 위해 1
cur_stage_obj = None # 현재 스테이지 객체
player_obj = None    # 현재 플레이어 객체
hp_image = None      # 플레이어 체력 이미지

poison_image_1 = None
poison_image_2 = None

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
        cur_stage_obj = None
    cur_stage = new_stage

    if cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT, player_obj)
    else:
        stage = Stage0(player_obj,WIDTH, HEIGHT)
    stage.enter()
    game_world.add_object(stage, 0)
    cur_stage_obj = stage

def init():   # 모든 객체 초기화
    global cur_stage, cur_stage_obj, player_obj, poison_image_1, poison_image_2

    # 혹시 이전 모드에서 world를 안 비우고 넘어온 경우 대비
    game_world.clear()

    # 플레이어 생성
    if player == 0:
        player_obj = Player(40, 40, 0)
    else:
        player_obj = Player(40, 40, 1)

    # 현재 cur_stage 값에 맞는 스테이지 하나 생성
    if cur_stage == 0:
        stage = Stage0(player_obj, WIDTH, HEIGHT)
    elif cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT, player_obj)

    # 월드에 등록
    game_world.add_object(stage, 0)
    game_world.add_object(player_obj, 1)
    game_world.add_collision_pairs('player:monster', player_obj, None)
    game_world.add_collision_pairs('player:object', player_obj, None)
    # 스테이지 enter
    stage.enter()
    cur_stage_obj = stage  # 현재 스테이지 객체

    # 독 이미지 로드
    poison_image_1 = load_image("poison_stage2_1.png")
    poison_image_2 = load_image("poison_stage2_2.png")

def update():   # 객체들의 상호작용, 행위 업데이트
    global cur_stage, cur_stage_obj

    game_world.update()

    if cur_stage_obj is not None:
        cur_stage_obj.check_collision(player_obj)

    if cur_stage == 0 and player_obj.at_stage0_exit():
        change_stage(1)
    #열쇠 찾았는지 확인 후 다음 스테이지로
    if cur_stage == 1 and player_obj.find_key:
        if cur_stage_obj is not None:
            cur_stage_obj.exit()
            cur_stage_obj = None
        # 스테이지 변경
        cur_stage = 2

        player_obj.find_key = False
        delay(1.5)
        game_framework.change_mode(first_to_second_mode)

    if cur_stage == 2 and player_obj.find_key:
        if cur_stage_obj is not None:
            cur_stage_obj.exit()
            cur_stage_obj = None

        cur_stage = 3

        player_obj.find_key = False
        delay(1.5)
        game_framework.change_mode(second_to_third_mode)

    set_player_hp_image()
    if player_obj.hp <= 0:
        delay(0.5)
        game_framework.change_mode(game_over_mode)
    game_world.handle_collisions()


def update_during_hint():   # 힌트 모드에서만 쓸
    game_world.update()

    # 스테이지 충돌 체크
    if cur_stage is not None:
        cur_stage_obj.check_collision(player_obj)

    # 충돌 처리만
    game_world.handle_collisions()

def draw():   # 객체들 그리기
    global hp_image
    clear_canvas()
    game_world.render()
    if hp_image is not None:
        hp_image.clip_composite_draw(0, 0, 327, 96,
                                     0, '', 100, 570, 120, 35)

    if player_obj.poison_1:
        poison_image_1.draw(500, 300, 700, 700)
    if player_obj.poison_2:
        poison_image_2.draw(500, 300, 1000, 600)


    update_canvas()

def finish():   # 게임 종료 시 처리
    game_world.clear()

def set_player_hp_image():
    global player_obj, hp_image
    if player_obj is not None:
        if player_obj.hp == 3:
            hp_image = load_image("heart_3.png")
        elif player_obj.hp == 2:
            hp_image = load_image("heart_2.png")
        elif player_obj.hp == 1:
            hp_image = load_image("heart_1.png")
        else:
            pass  # 게임 오버 할 예정


def pause():
    pass
def resume():
    pass