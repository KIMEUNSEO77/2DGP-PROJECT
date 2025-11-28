from pico2d import *
import game_framework
import play_mode
import title_mode

image = None
bgm = None

def init():
    global image, start_time, bgm
    image = load_image('game_clear_1.png')
    start_time = get_time()

    # 배경 음악 로드 & 재생
    bgm = load_music('sound/sound_game_clear.mp3')
    bgm.set_volume(64)  # 볼륨
    bgm.repeat_play()

def finish():
    global image
    del image
    global bgm
    # 모드 이동 시 음악 끄기
    if bgm:
        bgm.stop()

def update():
    global image, start_time
    if get_time() - start_time >= 2.5:
        if play_mode.player == 0:
            image = load_image('game_clear_2(1).png')
        elif play_mode.player == 1:
            image = load_image('game_clear_2(2).png')

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

def pause(): pass
def resume(): pass