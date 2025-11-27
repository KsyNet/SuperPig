from pygame import *
import pyganim
import os

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
ICON_DIR = os.path.join(os.path.dirname(__file__), 'sprites')  # Полный путь к каталогу с файлами

ANIMATION_MONSTERHORYSONTAL = [
    (image.load(os.path.join(ICON_DIR, "monsters", "fire1.png"))),
    (image.load(os.path.join(ICON_DIR, "monsters", "fire2.png")))
]

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x  # Начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # Максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # Максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # Скорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # Скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):  # по принципу героя

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # Если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # Если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # Если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel