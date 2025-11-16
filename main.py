from pico2d import *
import play_mode as start_mode   # start_mode로 별칭 지정
import title_mode
import game_framework

WIDTH, HEIGHT = 1000, 600
open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
close_canvas()