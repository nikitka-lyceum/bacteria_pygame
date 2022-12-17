import pygame as pg
import sys
import random as rnd

pg.init()
win = pg.display.set_mode((500, 500))
background = pg.image.load("background.png").convert()
##  Рекомендую использовать .convert(), иначе будет сильно лагать

class cam:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 500, 500)

    def move(self, vector):
        self.rect[0] += vector[0]
        self.rect[1] += vector[1]

class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 10, 10)

    def move(self, vector):
        self.rect[0] += vector[0]
        self.rect[1] += vector[1]

    def draw(self):
        ##  Игрок на самом окне не двигается, двигается мир вокруг него
        pg.draw.rect(win, (0, 0, 0), (240, 240, 10, 10))

class object:
    ##  Это какой-нибудь объект, отличный игрока (к примеру враг или дерево)
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def draw(self):
        ##  Чтобы отрисовка соответствовала позиции объекта его нужно отрисовывать
        ##  на self.rect[0]-camera.rect[0], self.rect[1]-camera.rect[1]
        pg.draw.rect(win, (255, 0, 0), (self.rect[0] - camera.rect[0], self.rect[1] - camera.rect[1], self.rect[2], self.rect[3]), 2)

##  P.S. я указывал переменные rect для того, чтобы можно было проверять коллизию между
##  объектами. К примеру: для увеличения производительности, в этой программе отрисовываются лишь те
##  объекты, которые попадают в камеру. (Загугли pg.Rect.colliderect для большего)

player = Player(0, 0)
camera = cam(0, 0)

objects = [object(250, 250, 30, 10)]

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                objects.append(object(rnd.randint(0, 400), rnd.randint(0, 400), rnd.randint(5, 15), rnd.randint(5, 15)))

    vector = [0, 0]

    kpressed = pg.key.get_pressed()
    if kpressed[pg.K_UP]:
        vector[1] -= 3
    elif kpressed[pg.K_DOWN]:
        vector[1] += 3

    if kpressed[pg.K_LEFT]:
        vector[0] -= 3
    elif kpressed[pg.K_RIGHT]:
        vector[0] += 3

    ##  Если игрок ходил
    if vector != [0, 0]:
        player.move(vector)
        camera.move(vector)

    win.fill((255, 255, 255))
    win.blit(background, (-camera.rect[0], -camera.rect[1]))
    player.draw()

    ##  ДЛЯ ПРО
    ##  отрисовка других объектов
    for obj in objects:
        ##  Если объект на экране, отрисовать его
        if obj.rect.colliderect(camera.rect):
            obj.draw()

    pg.display.flip() ##    = pg.display.update()
    pg.time.wait(30)