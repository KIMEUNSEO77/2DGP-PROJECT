from pico2d import *
import play_mode

open_canvas(play_mode.WIDTH, play_mode.HEIGHT)
play_mode.init()

while play_mode.running:
    play_mode.handle_events()
    play_mode.update()

    if play_mode.player_obj.at_stage0_exit():
        play_mode.change_stage(1)

    play_mode.cur_stage_obj.check_collision(play_mode.player_obj)

    play_mode.draw()
    delay(0.05)
play_mode.finish()
close_canvas()