import pygame
import pyganim

from player import *
from blocks import *

pygame.init()
# Объявляем переменные-константы для экрана
WIN_WIDHT = 800
WIN_HEIGTH = 640
DISPLAY = (WIN_WIDHT, WIN_HEIGTH)
BACKGROUND_COLOR = "#004400"

def main():
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Hollow Night")
    bg = Surface((WIN_WIDHT, WIN_HEIGTH))
    bg.fill(color=BACKGROUND_COLOR)

    # Объявляем персонажа
    hero = Player(55, 55)   # Создаём персонажа по координатам
    left = right = False    # По умолчанию стоим
    up = False

    entities = pygame.sprite.Group()    # Все объекты
    platforms = []   # ТО, во что будем врезаться или опираться
    entities.add(hero)

    # Объявляем уровень
    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-            --         -",
        "-                       -",
        "--                      -",
        "-                       -",
        "-                   --- -",
        "-                       -",
        "-                       -",
        "-      ---              -",
        "-                       -",
        "-   -----------         -",
        "-                       -",
        "-                -      -",
        "-                   --  -",
        "-                       -",
        "-                       -",
        "-------------------------"]

    timer = pygame.time.Clock()

    # Координаты
    x = y = 0
    for row in level:  # Каждая строка
        for col in row:  # Каждый символ
            if col == "-":
                # Создаём блок, заливаем его цветом и рисуем его
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # Блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высостой
        x = 0  # на каждой новой строчке начинаем с нуля

    while 1:
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем событие
            # Проверка нажатия клавиш
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == QUIT:
                raise SystemExit("QUIT")
        screen.blit(bg, (0, 0)) # Каждую итерацию перерисовываем

        hero.update(left, right, up, platforms)    # Передвижение
        entities.draw(screen)   # Отображение всего


        pygame.display.update()

if __name__ == "__main__":
    main()

