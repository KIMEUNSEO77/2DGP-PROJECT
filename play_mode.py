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

WIDTH, HEIGHT = 1000, 600
player = 1 # 0: mage, 1: knight
cur_stage = 3 # 현재 스테이지 번호 디버깅을 위해 1
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

        '''
        # 2) 스테이지 객체 자체도 월드에서 제거
        try:
            game_world.remove_object(cur_stage_obj)
        except:
            pass
'''
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

'''
def init():   # 모든 객체 초기화
    global cur_stage, cur_stage_obj, player_obj, poison_image_1, poison_image_2

    if player == 0:
        player_obj = Player(40, 40, 0)
    else:
        player_obj = Player(40, 40, 1)

    if cur_stage == 0:
        stage = Stage0(player_obj, WIDTH, HEIGHT)
    elif cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT, player_obj)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT, player_obj)
    game_world.add_object(stage, 0)
    game_world.add_object(player_obj, 1)
    game_world.add_collision_pairs('player:monster', player_obj, None)
    game_world.add_collision_pairs('player:object', player_obj, None)

    stage.enter()
    cur_stage_obj = stage

    poison_image_1 = load_image("poison_stage2_1.png")
    poison_image_2 = load_image("poison_stage2_2.png")
    '''
def init():   # 모든 객체 초기화
    global cur_stage, cur_stage_obj, player_obj, poison_image_1, poison_image_2

    # 혹시 이전 모드에서 world를 안 비우고 넘어온 경우 대비
    game_world.clear()

    # 플레이어 생성 (필요하면 나중에 hp/상태 유지용으로 구조 바꿔도 됨)
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

    # 월드에 등록 + 스테이지 enter
    game_world.add_object(stage, 0)
    game_world.add_object(player_obj, 1)
    game_world.add_collision_pairs('player:monster', player_obj, None)
    game_world.add_collision_pairs('player:object', player_obj, None)

    stage.enter()
    cur_stage_obj = stage  # 🔹 현재 스테이지 객체 기억

    # 독 이미지 로드
    poison_image_1 = load_image("poison_stage2_1.png")
    poison_image_2 = load_image("poison_stage2_2.png")


'''
def update():   # 객체들의 상호작용, 행위 업데이트
    game_world.update()

    if cur_stage is not None:
        cur_stage_obj.check_collision(player_obj)

    if cur_stage == 0 and player_obj.at_stage0_exit():
        change_stage(1)

    if cur_stage == 1 and player_obj.find_key:
        delay(1.5)  # 열쇠 찾고 나서 잠시 대기
        game_framework.change_mode(first_to_second_mode)
        change_stage(2)
        player_obj.find_key = False
    if cur_stage == 2 and player_obj.find_key:
        delay(1.5)
        game_framework.change_mode(second_to_third_mode)
        change_stage(3)
        player_obj.find_key = False

    set_player_hp_image()
    game_world.handle_collisions()
    '''

def update():   # 객체들의 상호작용, 행위 업데이트
    global cur_stage, cur_stage_obj  # 🔹 이거 꼭 추가!

    game_world.update()

    if cur_stage_obj is not None:
        cur_stage_obj.check_collision(player_obj)

    if cur_stage == 0 and player_obj.at_stage0_exit():
        change_stage(1)

    # 1 → 2 : 열쇠 찾으면 Stage1 정리 + cur_stage만 2로 바꾸고 연출 모드로
    if cur_stage == 1 and player_obj.find_key:
        # 1) 현재 스테이지 깔끔하게 정리
        if cur_stage_obj is not None:
            cur_stage_obj.exit()
            cur_stage_obj = None

        # 2) 다음에 init()에서 Stage2를 만들 수 있도록 번호만 바꿔 둠
        cur_stage = 2

        # 3) 플래그 리셋 + 연출 모드로 전환
        player_obj.find_key = False
        delay(1.5)
        game_framework.change_mode(first_to_second_mode)

    # 2 → 3 : 마찬가지로 Stage2 정리 후 번호만 바꾸고 연출 모드로
    if cur_stage == 2 and player_obj.find_key:
        if cur_stage_obj is not None:
            cur_stage_obj.exit()
            cur_stage_obj = None

        cur_stage = 3

        player_obj.find_key = False
        delay(1.5)
        game_framework.change_mode(second_to_third_mode)

    set_player_hp_image()
    game_world.handle_collisions()


def update_during_hint():   # 힌트 모드에서만 쓸 "안전 버전"
    # 1) 기본 오브젝트 업데이트
    game_world.update()

    # 2) 스테이지 충돌 체크 (바닥/구멍 떨어짐 방지)
    if cur_stage is not None:
        cur_stage_obj.check_collision(player_obj)

    # 3) 충돌 처리만 (HP, 데미지 등)
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