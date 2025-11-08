from pico2d import *
import game_framework
import play_mode
import title_mode

image = None

def init():
    global image, start_time
    if play_mode.player == 0:
        image = load_image('Mage_2.5stage_1.png')
    elif play_mode.player == 1:
        image = load_image('Knight_2.5stage_1.png')
    start_time = get_time()

def finish():
    global image
    del image

def update():
    global image, start_time
    if get_time() - start_time >= 1.5:
        if play_mode.player == 0:
            image = load_image('Mage_2.5stage_2.png')
        elif play_mode.player == 1:
            image = load_image('Knight_2.5stage_2.png')

    if get_time() - start_time >= 3.0:
            if play_mode.player == 0:
                image = load_image('Mage_2.5stage_3.png')
            elif play_mode.player == 1:
                image = load_image('Knight_2.5stage_3.png')
    if get_time() - start_time >= 4.5:
        play_mode.cur_stage = 3
        game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(500, 300)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)

def pause(): pass
def resume(): pass