from PIL.FontFile import WIDTH
from pygame import *

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35

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

    def update(self, left, right, up):
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

        self.rect.x += self.xvel    # Переносим свое положение на xvel

    def draw(self, screen): # Выводим персонажа на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))