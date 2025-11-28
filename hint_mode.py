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

    if hasattr(play_mode, 'player_obj') and play_mode.player_obj is not None:
        p = play_mode.player_obj
        # 상태를 IDLE로 강제 변경
        p.state_machine.cur_state = p.IDLE
        p.dir = 0
        p.prev_x, p.prev_y = p.x, p.y


def finish():
    global hint
    if hint:
        hint = None
    if play_mode.player_obj is not None:
        play_mode.player_obj.hintOpened = False

def update():
    play_mode.update_during_hint()

def draw():
    clear_canvas()
    game_world.render()

    if hint is not None:
        hint.draw()

    update_canvas()


def handle_events():
    event_list = get_events()   # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RETURN:
                print('[HINT] POP MODE!!!')
                game_framework.pop_mode()   # 이전 모드로 복귀

def pause():
    pass
def resume():
    pass

