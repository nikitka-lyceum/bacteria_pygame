from pygame import *

class Map:
    def __init__(self, *objects):
        self.objects = objects
        print(*self.objects)

    def update(self, event):
        for obj in self.objects:
            if event[K_a] or event[K_LEFT]:
                obj.rect = obj.rect.move(obj.speed, 0)

            if event[K_d] or event[K_RIGHT]:
                obj.rect = obj.rect.move(-obj.speed, 0)

            if event[K_w] or event[K_UP]:
                obj.rect = obj.rect.move(0, obj.speed)

            if event[K_s] or event[K_DOWN]:
                obj.rect = obj.rect.move(0, -obj.speed)