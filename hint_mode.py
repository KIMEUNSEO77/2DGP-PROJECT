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
    #game_world.add_object(hint, 2)

    # ---- 여기서 플레이어 강제 정지 (아래 2번에서 설명) ----
    if hasattr(play_mode, 'player_obj') and play_mode.player_obj is not None:
        p = play_mode.player_obj
        # 상태를 IDLE로 강제 변경
        p.state_machine.cur_state = p.IDLE
        p.dir = 0
        p.prev_x, p.prev_y = p.x, p.y
    # -----------------------------------------------------


def finish():
    global hint
    if hint:
        #game_world.remove_object(hint)
        hint = None
    if play_mode.player_obj is not None:
        play_mode.player_obj.hintOpened = False

def update():
    # 플레이 모드의 업데이트를 호출해서 플레이어 물리/충돌을 계속 수행
    #game_world.update()   # 왜냐하면, 힌트 모드에서는 play 모드가 유지돼야하므로.
    #play_mode.update()
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
        #print('[HINT] event:', event.type, getattr(event, 'key', None))
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

