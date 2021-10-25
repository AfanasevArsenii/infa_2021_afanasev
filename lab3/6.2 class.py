import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 50
screen = pygame.display.set_mode((900, 600))
score = 0  # переменная для подсчёта очков
balls_quantity = 5
rectangles_quantity = 5
my_balls = [0]*balls_quantity
my_rectangles = [0]*rectangles_quantity

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Balls:
    """Класс шариков
    :param self.x: начальная координата по оси Ox
    :param self.y: начальная координата по оси Oy
    :param self.r: радиус шарика
    :param self.color: цвет шарика
    :param self.dx: начальная скорость шарика по оси Ox
    :param self.dy: начальная скорость шарика по оси Oy
    :param self.screen: поверхность, на которой создаётся изображение
    """
    def __init__(self, screen):
        self.x = randint(100, 800)
        self.y = randint(100, 500)
        self.r = randint(10, 100)
        self.color = COLORS[randint(0, 5)]
        self.dx = randint(-10, 10)
        self.dy = randint(-10, 10)
        self.screen = screen

    def move(self):
        """Функция двигает шарик (меняет координаты)
        Если шарик ударился о стенку меняет скорость шарика"""
        self.x += self.dx
        self.y += self.dy
        if self.x - self.r < 0:
            self.dx = randint(1, 10)
        if self.x + self.r > 900:
            self.dx = randint(-10, -1)
        if self.y - self.r < 0:
            self.dy = randint(1, 10)
        if self.y + self.r > 600:
            self.dy = randint(-10, -1)

    def draw(self):
        """Функция отрисовывает новое положение шарика"""
        circle(self.screen, self.color, (self.x, self.y), self.r)


class Rectangles:
    """Класс прямоугольников
    :param self.x: начальная координата по оси Ox
    :param self.y: начальная координата по оси Oy
    :param self.width: ширина прямоугольника
    :param self.height: высота прямоугольника
    :param self.color: цвет прямоугольника
    :param self.dx: начальная скорость прямоугольника по оси Ox
    :param self.dy: начальная скорость прямоугольника по оси Oy
    :param self.screen: поверхность, на которой создаётся изображение
    """
    def __init__(self, screen):
        self.x = randint(100, 800)
        self.y = randint(100, 500)
        self.width = randint(10, 100)
        self.height = randint(10, 100)
        self.color = COLORS[randint(0, 5)]
        self.dx = randint(-10, 10)
        self.dy = randint(-10, 10)
        self.screen = screen


    def move(self):
        """Функция двигает прямоуголник (меняет координаты)
        Если прямоугольник ударился о стенку меняет скорость прямоугольника"""
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.dx = randint(1, 10)
        if self.x + self.width > 900:
            self.dx = randint(-10, -1)
        if self.y < 0:
            self.dy = randint(1, 10)
        if self.y + self.height > 600:
            self.dy = randint(-10, -1)


    def draw(self):
        """Функция отрисовывает новое положение шарика"""
        rect(self.screen, self.color, (self.x, self.y, self.width, self.height))



for i in range(balls_quantity):  # создаём заданное количество шариков
    my_balls[i] = Balls(screen)

for i in range(rectangles_quantity):  # создаём заданное количество прямоугольников
    my_rectangles[i] = Rectangles(screen)



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #click(event)
    for i in range(balls_quantity):  # двигаем шарики
        my_balls[i].move()
        my_balls[i].draw()
    for i in range(rectangles_quantity):  # двигаем прямоугольники
        my_rectangles[i].move()
        my_rectangles[i].draw()
    #draw_score(score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
