from event import right_down, left_down, right_up, left_up, up_down, down_down, up_up, down_up

w, h = 32, 40

class Idle:   # 가만히 서 있는 상태
    def __init__(self, player):
        self.player = player
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.player.frame = 1

    def draw(self):
        global w, h
        if self.player.face_dir == 1:   # 오른쪽 바라볼 때
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)
        else:   # 왼쪽 바라볼 때
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, 'h', self.player.x, self.player.y, w * 1.5, h * 1.5)


class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.player.dir = self.player.face_dir = 1
        elif left_down(e) or right_up(e):
            self.player.dir = self.player.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 3
        self.player.x += self.player.dir * 5

    def draw(self):
        global w, h
        if self.player.face_dir == 1:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, '', self.player.x, self.player.y, w * 1.5, h * 1.5)
        else:
            self.player.image.clip_composite_draw(self.player.frames[self.player.frame], 45, w, h,
                                                  0, 'h', self.player.x, self.player.y, w * 1.5, h * 1.5)

class Jump:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 1

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass
