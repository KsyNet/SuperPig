import pygame
from pygame import *
import pyganim
import os

ICON_DIR = os.path.join(os.path.dirname(__file__), 'sprites')
# Объявляем переменные-константы для платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

ANIMATION_BLOCKTELEPORT = [
    (image.load(os.path.join(ICON_DIR, "blocks", "portal2.png"))),
    (image.load(os.path.join(ICON_DIR, "blocks", "portal1.png")))]

ANIMATION_FLAG = [
    (image.load(os.path.join(ICON_DIR, "blocks", "flag2.png"))),
    (image.load(os.path.join(ICON_DIR, "blocks", "flag1.png")))
]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(color=PLATFORM_COLOR)
        self.image = image.load(os.path.join(ICON_DIR, "blocks", "block.png"))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load(os.path.join(ICON_DIR, "blocks", "block_die.png"))


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class FlagWin(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_FLAG:
            boltAnim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


