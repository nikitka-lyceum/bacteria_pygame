from config import *

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, x, y):
        return x + self.dx, y + self.dy

    # позиционировать камеру на объекте target
    def update(self, x, y, w, h):
        self.dx = -(x + w // 2 - WIDTH // 2)
        self.dy = -(y + h // 2 - HEIGHT // 2)