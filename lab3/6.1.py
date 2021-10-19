import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 50
screen = pygame.display.set_mode((900, 600))
score = 0  # переменная для подсчёта очков
balls_quantity = 5
squares_quantity = 5
balls = []
squares = []
#  объявляем базовые цвета шариков
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_balls(balls_quantity):
    """Функция рисует новый шарик."""
    for i in range(balls_quantity):
        x = randint(100, 800)
        y = randint(100, 500)
        r = randint(1, 100)
        color = COLORS[randint(0, 5)]
        dx = randint(-10, 10)
        dy = randint(-10, 10)
        balls.append([x, y, r, color, dx, dy])


def new_squares(squares_quantity):
    for i in range(squares_quantity):
        x = randint(100, 800)
        y = randint(100, 500)
        width = randint(10, 100)
        height = randint(10, 100)
        color = COLORS[randint(0, 5)]
        dx = randint(-10, 10)
        dy = randint(-10, 10)
        squares.append([x, y, width, height, color, dx, dy])


def move_ball():
    """Функция двигает шарик"""
    for i in range(balls_quantity):
        balls[i][0] = balls[i][0] + balls[i][4]
        balls[i][1] += balls[i][5]
        if balls[i][0] - balls[i][2] < 0:
            balls[i][4] = randint(1, 10)
        if balls[i][0] + balls[i][2] > 900:
            balls[i][4] = randint(-10, -1)
        if balls[i][1] - balls[i][2] < 0:
            balls[i][5] = randint(1, 10)
        if balls[i][1] + balls[i][2] > 600:
            balls[i][5] = randint(-10, -1)
        circle(screen, balls[i][3], (balls[i][0], balls[i][1]), balls[i][2])

def move_square():
    """Функция двигает шарик"""
    for i in range(squares_quantity):
        squares[i][0] = squares[i][0] + squares[i][5]
        squares[i][1] += squares[i][6]
        if squares[i][0] < 0:
            squares[i][5] = randint(1, 10)
        if squares[i][0] + squares[i][2] > 900:
            squares[i][5] = randint(-10, -1)
        if squares[i][1] < 0:
            squares[i][6] = randint(1, 10)
        if squares[i][1] + squares[i][3] > 600:
            squares[i][6] = randint(-10, -1)
        rect(screen, squares[i][4], (squares[i][0], squares[i][1], squares[i][2], squares[i][3]))


def move_ball():
    """Функция двигает шарик"""
    for i in range(balls_quantity):
        balls[i][0] = balls[i][0] + balls[i][4]
        balls[i][1] += balls[i][5]
        if balls[i][0] - balls[i][2] < 0:
            balls[i][4] = randint(1, 10)
        if balls[i][0] + balls[i][2] > 900:
            balls[i][4] = randint(-10, -1)
        if balls[i][1] - balls[i][2] < 0:
            balls[i][5] = randint(1, 10)
        if balls[i][1] + balls[i][2] > 600:
            balls[i][5] = randint(-10, 1)
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
    global score
    for i in range(balls_quantity):
        if (cur_event.pos[0]-balls[i][0])**2 + (cur_event.pos[1]-balls[i][1])**2 <= balls[i][2]**2:
            score += 1
            balls.pop(i)
            new_balls(1)
            hasClicked = True
    for i in range(squares_quantity):
        if (cur_event.pos[0]-squares[i][0])**2 + (cur_event.pos[1]-squares[i][1])**2 <= squares[i][2]**2:
            score += 3
            squares.pop(i)
            new_squares(1)
            hasClicked = True
    if not hasClicked:
        score -= 1


"""
def results_table():
    print("Введите своё имя: ")
    output = open("results.txt", 'r')
    records = output.readlines()
    output = open("results.txt", 'a')
    records.append(input() + ": " + str(score) + '\n')
    output.write(input() + " " + str(score) + '\n')
    for i in (len(records)):
        records[i] = records[i].split(': ')
    

    records.sort()
    output.close()
    """


new_balls(balls_quantity)
new_squares(squares_quantity)

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
    move_square()
    draw_score(score)
    pygame.display.update()
    screen.fill(BLACK)

#results_table()
pygame.quit()
