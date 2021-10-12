import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
screen = pygame.display.set_mode((800, 800))
score = 0  # переменная для подсчёта очков

#  объявляем базовые цвета шариков
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """Функция рисует новый шарик."""
    global x, y, r
    x = randint(100, 700)
    y = randint(100, 700)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def draw_score(score):
    """
    Функция рисует панель счётчика с обновляющимся счётом:
    :param score: счёт (количество пойманных шариков)
    """
    f = pygame.font.SysFont('arial', 36)
    text = f.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(text, (250, 50))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0]-x)**2 + (event.pos[1]-y)**2 <= r**2:  # проверяем, поймали ли шарик
                print('Yeah, boy!')
                score += 1  # добавляем очки
            else:
                print('Miss again!')

    new_ball()
    draw_score(score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
