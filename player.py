import pyganim
from PIL.FontFile import WIDTH
from pygame import *
#from pyganim import *

MOVE_SPEED = 7
WIDTH = 31
HEIGHT = 18
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35

# Переменные для анимации
ANIMATION_DELAY = 1 # скорость смены кадров анимации
ANIMATION_RIGHT = [('sprites/pig/pig_right_1.png'),
            ('sprites/pig/pig_right_2.png')]
ANIMATION_LEFT = [('sprites/pig/pig_left_1.png'),
            ('sprites/pig/pig_left_2.png')]
ANIMATION_JUMP_LEFT = [('sprites/pig/pig_jump_left.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('sprites/pig/pig_jump_right.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('sprites/pig/pig_jump_right.png', ANIMATION_DELAY)] # Добавить или убрать анимацию прыжка
ANIMATION_STAY = [('sprites/pig/pig_stay.png', ANIMATION_DELAY)]


class Player(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # Скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(color=COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # Прямоугольный объект
        self.yvel = 0  # Скорость вертикального перемещения
        self.onGround = False  # На земле?

        self.image.set_colorkey(COLOR)  # Делаем фон прозрачным
        # Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        # Анимация стоять
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        # Анимация прыгать влево
        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        # Анимация прыгать вправо
        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()



    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:  # Прыгаем, только когда стоим на земле
                self.yvel = -JUMP_POWER
            # Анимация прыжка
            self.image.fill(color=COLOR)
            self.boltAnimJumpRight.blit(self.image, (0, 0))

        if left:
            self.xvel = - MOVE_SPEED  # Лево = x-n
            # Анимация для прыжка влево
            self.image.fill(color=COLOR)
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x+n
            # Анимация идти вправо
            self.image.fill(color=COLOR)
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # Стоим, когда нет указаний идти
            self.xvel = 0
            # Анимация стоять
            if not up:
                self.image.fill(color=COLOR)
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround: # Ускоряем падение, когда не на поверхности
            self.yvel += GRAVITY
        self.onGround = False  # Мы не знаем, когда мы на земле

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel  # Переносим свое положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Если есть пересечение платформы с игроком

                if xvel > 0:  # Если движется вправо
                    self.rect.right = p.rect.left  # То не движется вправо

                if xvel < 0:  # Если движется влево
                    self.rect.left = p.rect.right  # То не движется вправо

                if yvel > 0:  # Если падает вниз
                    self.rect.bottom = p.rect.top  # То не падает вниз
                    self.onGround = True  # И становится на что-то твердое
                    self.yvel = 0  # И энергия падения пропадает

                if yvel < 0:  # Если движется вверх
                    self.rect.top = p.rect.bottom  # То не движется вверх
                    self.yvel = 0  # И энергия прыжка пропадает

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))