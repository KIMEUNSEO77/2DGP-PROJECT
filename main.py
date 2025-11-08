from pico2d import *
import play_mode as start_mode  # start_mode로 별칭 지정
import title_mode
import game_framework

WIDTH, HEIGHT = 1000, 600
open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
'''
play_mode.init()
title_mode.init()
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()

    if play_mode.player_obj.at_stage0_exit():
        play_mode.change_stage(1)

    play_mode.cur_stage_obj.check_collision(play_mode.player_obj)

    play_mode.draw()
    delay(0.05)
play_mode.finish()
while title_mode.running:
    title_mode.handle_events()
    title_mode.update()
    title_mode.draw()
    delay(0.05)
title_mode.finish()
'''
close_canvas()