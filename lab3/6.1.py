import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((900, 600))
score = 0  # переменная для подсчёта очков
balls_quantity = 5
balls = []

#  объявляем базовые цвета шариков
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_balls():
    """Функция рисует новый шарик."""
    for i in range (balls_quantity):
        x = randint(100, 800)
        y = randint(100, 500)
        r = randint(1, 100)
        color = COLORS[randint(0, 5)]
        dx = randint(-10, 10)
        dy = randint(-10, 10)
        balls.append([x, y, r, color, dx, dy])



def move_ball():
    """Функция двигает шарик"""
    for i in range(balls_quantity):
        balls[i][0] = balls[i][0] + balls[i][4]
        balls[i][1] += balls[i][5]
        if balls[i][0] - balls[i][2] < 0 or balls[i][0] + balls[i][2] > 900:
            balls[i][4] = - balls[i][4]
        if balls[i][1] - balls[i][2] < 0 or balls[i][1] + balls[i][2] > 600:
            balls[i][5] = - balls[i][5]
        circle(screen, balls[i][3], (balls[i][0], balls[i][1]), balls[i][2])


def draw_score(score):
    """
    Функция рисует панель счётчика с обновляющимся счётом:
    :param score: счёт (количество пойманных шариков)
    """
    f = pygame.font.SysFont('arial', 36)
    text = f.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(text, (250, 50))


def click(cur_event):
    """
    Функция реагирует на нажатие на шарик.
    Если попал - прибавляется балл, если нет - балл отнимается.
    """
    hasClicked = False
    for i in range(balls_quantity):
        global score
        if (cur_event.pos[0]-balls[i][0])**2 + (cur_event.pos[1]-balls[i][1])**2 <= balls[i][2]**2:
            score += 1
            hasClicked = True
    if not hasClicked:
        score -= 1
        print('Miss again!')


new_balls()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    move_ball()
    draw_score(score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
