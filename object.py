from pico2d import load_image


class Object:
    def __init__(self, w, h, x, y, image_file, id): # id 0이면 위만 충돌체크, 1이면 전체 충돌체크
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.image = load_image(image_file)
        self.id = id

    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass

    # 중심(x,y), 폭w, 높이h 기준 AABB
    def aabb(self):
        half_w, half_h = self.w * 0.5, self.h * 0.5
        left = self.x - half_w
        right = self.x + half_w
        bottom = self.y - half_h
        top = self.y + half_h
        return left, bottom, right, top
