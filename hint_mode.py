from pico2d import *
import game_framework
import game_world
from hint import Hint
import play_mode

hint_index = None
hint = None

def init():
    global hint

    if hint_index is not None:
        hint = Hint(hint_index)
    game_world.add_object(hint, 2)

def finish():
    global hint
    if hint:
        game_world.remove_object(hint)
        hint = None

def update():
    # 플레이 모드의 업데이트를 호출해서 플레이어 물리/충돌을 계속 수행
    game_world.update()   # 왜냐하면, 힌트 모드에서는 play 모드가 유지돼야하므로.

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    event_list = get_events()   # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()   # 이전 모드로 복귀


def pause():
    pass
def resume():
    pass