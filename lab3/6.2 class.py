import pygame
from pygame.draw import *
from random import randint

score = 0  # переменная для подсчёта очков
balls_quantity = 5
rectangles_quantity = 5

my_balls = []
my_rectangles = []

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
        for j in range(len(my_balls)-1):
            if (self.x-my_balls[j].x)**2+(self.y-my_balls[j].y)**2 <= (self.r + my_balls[j].r)**2:
                self.dx, my_balls[j].dx = my_balls[j].dx, self.dx
                self.dy, my_balls[j].dy = my_balls[j].dy, self.dy

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


def draw_score(score):
    """
    Функция рисует панель счётчика с обновляющимся счётом:
    :param score: счёт (количество пойманных фигур)
    """
    f = pygame.font.SysFont('arial', 36)
    text = f.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(text, (250, 50))


def click(cur_event):
    global my_rectangles
    """
    Функция реагирует на нажатие на шарик или на прямоугольник.
    Если попал в шарик - прибавляется балл, если попал в прямоугольник - 3 балла,
    если нет - балл отнимается.
    :param cur_event: событие (клик)
    """
    clicked = False
    global score
    for i in range(len(my_balls)):
        if (cur_event.pos[0]-my_balls[i].x)**2 + (cur_event.pos[1]-my_balls[i].y)**2 <= my_balls[i].r**2:
            score += 1
            my_balls.pop(i)
            my_balls.append(Balls(screen))
            clicked = True
    for i in range(len(my_rectangles)):
        if (cur_event.pos[0] >= my_rectangles[i].x)\
                and (cur_event.pos[0] <= my_rectangles[i].x+my_rectangles[i].width)\
                and (cur_event.pos[1] >= my_rectangles[i].y)\
                and (cur_event.pos[1] <= my_rectangles[i].y + my_rectangles[i].height):
            score += 3
            my_rectangles.pop(i)
            my_rectangles.append(Rectangles(screen))
            clicked = True
    if not clicked:
        score -= 1


def custom_key(k):
    return k[1]


def results_table():
    results = []
    with open("resultsClasses.txt", 'r') as output:
        records = output.readlines()

    if len(records) == 0:
        with open("resultsClasses.txt", 'w') as output:
            output.write(name + ": " + str(score) + '\n')
    else:
        names = list(map(lambda x: x.split(': ')[0], records))
        scores = list(map(lambda x: x.split(': ')[1], records))
        scores = list(map(lambda x: x.split('\n')[0], scores))
        for i in range(len(records)):
            results.append([names[i], int(scores[i])])
        results.append([name, score])
        results.sort(key=custom_key, reverse=True)
        output = open("resultsClasses.txt", 'w')
        for i in range(len(results)):
            output.write(results[i][0] + ": " + str(results[i][1]) + '\n')
        output.close()


print("Введите своё имя: ")
name = input()

pygame.init()

FPS = 50
screen = pygame.display.set_mode((900, 600))

for i in range(balls_quantity):  # создаём заданное количество шариков
    my_balls.append(Balls(screen))


for i in range(rectangles_quantity):  # создаём заданное количество прямоугольников
    my_rectangles.append(Rectangles(screen))


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
    for i in range(balls_quantity):  # двигаем шарики
        my_balls[i].move()
        my_balls[i].draw()
    for i in range(rectangles_quantity):  # двигаем прямоугольники
        my_rectangles[i].move()
        my_rectangles[i].draw()
    draw_score(score)
    pygame.display.update()
    screen.fill(BLACK)

results_table()
pygame.quit()
