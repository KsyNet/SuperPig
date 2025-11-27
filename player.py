import pyganim
from PIL.FontFile import *
from pygame import *

import blocks
import monsters

MOVE_SPEED = 7
WIDTH = 31
HEIGHT = 18
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35

# Переменные для ускорения
MOVE_EXTRA_SPEED = 2.5  # Ускорение
JUMP_EXTRA_POWER = 1    # Дополнительная сила прыжка
ANIMATION_SUPER_SPEED_DELAY = 1.5  # Скорость смены кадров при ускорении

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
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        # Анимация движения влево
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

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

        self.winner = False

    def update(self, left, right, up, running, platforms):
        if up:
            if self.onGround:  # Прыгаем, только когда стоим на земле
                self.yvel = -JUMP_POWER
                if running and (left or right): # Если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER   # то прыгаем выше
            # Анимация прыжка
            self.image.fill(color=COLOR)
            self.boltAnimJumpRight.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if running:  # если ускорение
                self.xvel -= MOVE_EXTRA_SPEED  # то передвигаемся быстрее
                if not up:  # и если не прыгаем
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))  # то отображаем быструю анимацию
            else:  # если не бежим
                if not up:  # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0))  # отображаем анимацию движения
            if up:  # если же прыгаем
                self.boltAnimJumpLeft.blit(self.image, (0, 0))  # отображаем анимацию прыжка

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

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
                # если пересекаем блок смерти или моба
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster):
                        self.die()  # умираем
                elif isinstance(p, blocks.BlockTeleport):   # Если касаемся портала
                    self.teleporting(p.goX, p.goY)  # перемещаемся по координатам
                elif isinstance(p, blocks.FlagWin):   # Если касаемся флага
                    self.winner = True  # прошли уровень

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

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)  # Перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))