from pico2d import *
import game_framework
import play_mode
import title_mode

image = None

def init():
    global image
    image = load_image('game_over.png')

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(500, 300)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(title_mode)

def pause(): pass
def resume(): pass