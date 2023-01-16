from config import *

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть x, y на смещение камеры
    def apply(self, x, y):
        return x + self.dx, y + self.dy

    # позиционировать камеру
    def update(self, x, y, w, h, WIDTH, HEIGHT):
        self.dx = -(x + w // 2 - WIDTH // 2)
        self.dy = -(y + h // 2 - HEIGHT // 2)