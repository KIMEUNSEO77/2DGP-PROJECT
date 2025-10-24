from pico2d import *

from knight import Knight
from mage import Mage
from stage import Stage
from stage import Stage1
from stage import Stage2
from stage import Stage3

WIDTH, HEIGHT = 1000, 600
player = 0 # 0: mage, 1: knight
cur_stage = 1
world = []


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
    global world, mage, cur_stage, knight

    # 기존 월드 객체들 정리
    if 'world' in globals() and world:
        old_stage = None
        for obj in world:
            if isinstance(obj, Stage):
                old_stage = obj
                break
        if old_stage and hasattr(old_stage, 'exit'):
            old_stage.exit()
        for obj in world:
            if obj is old_stage:
                continue
            if hasattr(obj, 'exit'):
                obj.exit()

    cur_stage = new_stage
    if cur_stage == 1:
        stage = Stage1(WIDTH, HEIGHT)
    elif cur_stage == 2:
        stage = Stage2(WIDTH, HEIGHT)
    elif cur_stage == 3:
        stage = Stage3(WIDTH, HEIGHT)
    stage.enter()
    world.append(stage)

    # 플레이어를 월드에 다시 추가하고 위치/방향/상태/이벤트 초기화
    start_positions = {
        0: (50, 80),  # 스테이지별 시작 좌표 필요하면 확장
        1: (50, 80),
    }
    sx, sy = start_positions.get(cur_stage, (50, 80))

    if player == 0:
        # mage가 이미 있으면 재사용, 없으면 새로 생성
        if 'mage' not in globals() or mage is None:
            mage = Mage()
        # 위치/방향 초기화
        mage.x, mage.y = sx, sy
        if hasattr(mage, 'dir'):
            mage.dir = 1
        # 이벤트 큐 초기화(있으면)
        if hasattr(mage, 'event_que'):
            try:
                mage.event_que.clear()
            except Exception:
                mage.event_que = []
        # 상태 초기화(안정적으로 시도)
        if hasattr(mage, 'change_state'):
            try:
                mage.change_state('Idle')
            except Exception:
                try:
                    mage.change_state(0)
                except Exception:
                    pass
        elif hasattr(mage, 'state'):
            try:
                mage.state = 'Idle'
            except Exception:
                mage.state = None
        world.append(mage)
    else:
        if 'knight' not in globals() or knight is None:
            knight = Knight()
        knight.x, knight.y = sx, sy
        if hasattr(knight, 'dir'):
            knight.dir = 1
        if hasattr(knight, 'event_que'):
            try:
                knight.event_que.clear()
            except Exception:
                knight.event_que = []
        if hasattr(knight, 'change_state'):
            try:
                knight.change_state('Idle')
            except Exception:
                try:
                    knight.change_state(0)
                except Exception:
                    pass
        elif hasattr(knight, 'state'):
            try:
                knight.state = 'Idle'
            except Exception:
                knight.state = None
        world.append(knight)

def reset_world():   # 모든 객체 초기화
    global running, cur_stage, mage, knight
    running = True

    global world   # 모든 객체를 담을 수 있는 리스트

    # cur_stage = 0
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

    if player == 0 and mage.at_stage0_exit():
        change_stage(1)
    if player == 1 and knight.at_stage0_exit():
        change_stage(1)

    render_world()
    delay(0.05)

close_canvas()
