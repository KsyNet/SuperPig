import pyganim
from PIL.FontFile import WIDTH
from pygame import *
from pyganim import *

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35

# Переменные для анимации
ANIMATON_DELAY = 0.1    # Скорость смены кадров
ANIMATION_RIGHT = [('sprites/pig/pig_right_1.png'),
                   ('sprites/pig/pig_right_2.png')]
ANIMATION_LEFT = [('sprites/pig/pig_left_1.png'),
                  ('sprites/pig/pig_left_2.png')]
ANIMATION_JUMP_LEFT = [('sprites/pig/pig_jump_left.png')]
ANIMATION_JUMP_RIGHT = [('sprites/pig/pig_jump_right.png')]
ANIMATION_STAY = [('sprites/pig/pig_stay.png')]

class Player(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   # Скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(color=COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)   # Прямоугольный объект
        self.yvel = 0   # Скорость вертикального перемещения
        self.onGround = False   # На земле?

        self.image.set_colorkey(color=COLOR)    # Делаем фон прозрачным
        # Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATON_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATON_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По умолчанию стоим



    def update(self, left, right, up, platforms):
        if up:
            if self.onGround: # Прыгаем, только когда стоим на земле
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = - MOVE_SPEED    # Лево = x-n

        if right:
            self.xvel = MOVE_SPEED  # Право = x+n

        if not(left or right):  # Стоим, когда нет указаний идти
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False;  # Мы не знаем, когда мы на земле

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel    # Переносим свое положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):    # Если есть пересечение платформы с игроком

                if xvel > 0:                        # Если движется вправо
                    self.rect.right = p.rect.left   # То не движется вправо

                if xvel < 0:                        # Если движется влево
                    self.rect.left = p.rect.right   # То не движется вправо

                if yvel > 0:                        # Если падает вниз
                    self.rect.bottom = p.rect.top   # То не падает вниз
                    self.onGround = True            # И становится на что-то твердое
                    self.yvel = 0                   # И энергия падения пропадает

                if yvel < 0:                        # Если движется вверх
                    self.rect.top = p.rect.bottom   #  То не движется вверх
                    self.yvel = 0                   # И энергия прыжка пропадает

