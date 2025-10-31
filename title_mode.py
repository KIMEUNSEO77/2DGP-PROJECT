from pico2d import *

image = None
running = True
title_start_time = 0.0

def init():
    global image, running, title_start_time
    image = load_image('title_scene.png')
    running = True
    title_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running, title_start_time
    if get_time() - title_start_time > 2.0:
        title_start_time = get_time()
        running = False

def draw():
    clear_canvas()
    image.draw(500, 300)
    update_canvas()

def handle_events():
    events = get_events()   # 현재 이벤트들을 소비