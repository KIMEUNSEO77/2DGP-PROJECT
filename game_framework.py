from pico2d import *

running = None
stack = None


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()     # 현재 모드 삭제
    stack.append(mode)  # 새로운 모드 추가
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()   # 현재 모드의 pause 호출
    stack.append(mode)      # 새로운 모드를 스택에 추가
    mode.init()             # 새로운 모드 초기화


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()   # 현재 모드 finish
        # remove the current mode
        stack.pop()          # 현재 모드 삭제

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()   # stack Top에는 이전 모드가 있으므로, 이전 모드에 대해 resume 호출


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]   # start_mode를 담고 있는 스택을 생성
    start_mode.init()

    while running:
        # 현재 게임 모드(stack top에 있는 게임 모드)에 대한 루프 진행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        delay(0.05)   # 임시로 플레임 딜레이

    # repeatedly delete the top of the stack
    # 스택에 남아있는 모든 게임 모드들을 차례로 제거
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()