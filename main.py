from enum import Flag

import pygame
import pyganim
from pygame import *

import blocks
from monsters import Monster
from player import *
from blocks import *
from camera import *


# Объявляем переменные-константы для экрана
WIN_WIDHT = 800 # Ширина создаваемого окна
WIN_HEIGTH = 640 # Высота
DISPLAY = (WIN_WIDHT, WIN_HEIGTH)
BACKGROUND_COLOR = "#000000"
FILE_DIR = os.path.join(os.path.dirname(__file__), "levels")


def loadLevel():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open(os.path.join(FILE_DIR, "level_1.txt"))
    line = " "
    commands = []
    while True:
        line = levelFile.readline()
        if not line:
            break  # конец файла
        line = line.strip()  # удаляем лишние пробелы и символы новой строки
        if len(line) == 0:
            continue  # пропускаем пустые строки

        if line[0] == "/":  # символ завершения файла
            break

        if line[0] == "[":  # если нашли символ начала уровня
            while True:
                line = levelFile.readline()
                if not line:
                    break  # конец файла
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == "]":  # конец уровня
                    break
                endLine = line.find("|")
                if endLine != -1:
                    level.append(line[0:endLine])
                else:
                    level.append(line)

        # Обработка команд
        if len(line) > 0 and line[0] != "/":
            commands = line.split()
            if len(commands) > 1:
                if commands[0] == "player":
                    playerX = int(commands[1])
                    playerY = int(commands[2])
                elif commands[0] == "portal":
                    tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)
                elif commands[0] == "monster":
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)

def main():
    loadLevel()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Pig")
    bg = Surface((WIN_WIDHT, WIN_HEIGTH))

    bg.fill(color=BACKGROUND_COLOR)

    left, right = False, False    # По умолчанию стоим
    up = False
    running = False
    # Объявляем персонажа
    hero = Player(playerX, playerY)   # Создаём персонажа по координатам
    entities.add(hero)

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
                # Создаём блок смерти
            if col == "*":
                bd = BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
                # Создаём флаг
            if col == "F":
                fl = FlagWin(x,y)
                entities.add(fl)
                platforms.append(fl)
                animatedEntities.add(fl)

            x += PLATFORM_WIDTH  # Блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высостой
        x = 0  # на каждой новой строчке начинаем с нуля

    # Высчитываем фактическую ширину уровня
    total_level_widht = len(level[0]) * PLATFORM_WIDTH
    # Высчитываем фактическую высоту уровня
    total_level_heigth = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_widht, total_level_heigth)

    while not hero.winner:
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем событие
            # Проверка нажатия клавиш
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0)) # Каждую итерацию перерисовываем

        camera.update(hero) # Центрируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms)    # Передвижение
        # entities.draw(screen)   # Отображение всего
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        animatedEntities.update()  # Показываем анимацию
        monsters.update(platforms)  # Передвигаем всех мобов
        pygame.display.update()

level = []
entities = pygame.sprite.Group()    # Все объекты
animatedEntities = pygame.sprite.Group()    # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group()    # Все передвигающиеся объекты
platforms = []  # То, во что будем врезаться

if __name__ == "__main__":
    main()

