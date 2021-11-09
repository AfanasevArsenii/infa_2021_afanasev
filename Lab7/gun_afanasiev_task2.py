import math
import time
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
points = 0


class Projectile:
    def __init__(self, x, y):
        """ Конструктор класса Projectile снарядов.
        Args:
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        self.screen = screen
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.ay = 10
        self.lifetime = 0
        self.x = x
        self.y = y

    def move(self):
        """Метод перемещает снаряд.
        Метод описывает перемещение снаряда за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на снаряд,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.ay
        self.x += self.vx
        self.y -= self.vy

        if self.x - self.r < 0:
            self.vx = - self.vx
            self.x = self.r
        if self.x + self.r > WIDTH:
            self.vx = - self.vx
            self.x = WIDTH - self.r
        if self.y - self.r < 0:
            self.vy = -self.vy
            self.y = self.r
        if self.y + self.r >= HEIGHT:
            self.vy = -0.9*self.vy
            self.vx = 0.9*self.vx
            self.y = HEIGHT - self.r
            if abs(self.vy) < 5:
                self.vy = 0
                self.ay = 0

    def life(self):
        """Метод подсчитывает, сколько времени существует снаряд."""
        self.lifetime += 1
        return self.lifetime

    def draw(self):
        """Метод отрисовывает положение снаряда на экране."""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Метод проверяет сталкивалкивается ли снаряд с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((obj.__class__.__name__ == "TargetBall")
                and (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2):
            return True
        elif ((obj.__class__.__name__ == "TargetRectangle") and (self.x >= obj.x)
                and (self.x <= obj.x+obj.width)
                and (self.y >= obj.y)
                and (self.y <= obj.y + obj.height)):
            return True
        elif (((obj.__class__.__name__ == "GunEnemy") or (obj.__class__.__name__ == "Gun"))
                and (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.body_height*2**0.5)**2):
            return True
        else:
            return False


class Bullet(Projectile):
    def __init__(self, x, y):
        """Конструктор класса Bullet (дочерний класс класса Projectile)"""
        super().__init__(x, y)


class BulletEnemy(Projectile):
    def __init__(self, x, y):
        """ Конструктор класса BulletEnemy дочернего класса для класса Projectile).
        Args:
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        super().__init__(x, y)
        self.color = BLUE

    def hittest_bullet_enemy(self, obj):
        """Метод проверяет сталкивалкивается ли снаряд с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.body_height*2**0.5)**2:
            return True
        else:
            return False


class BulletFromBomb(Projectile):
    def __init__(self, x, y, color):
        """Конструктор класса BulletFromBomb (дочерний класс класса Projectile),
        создаёт пули(на месте бомбы с цветом бомбы со случайными скоростями),
        которые появляются после исчезновения бомбы или в случае попадания бомбой в цель.

        Args:"""
        super().__init__(x, y)
        self.r = 10
        self.vx = randint(-100, 100)
        self.vy = randint(-100, 100)
        self.color = color


class Bomb(Projectile):
    def __init__(self, x, y):
        """Конструктор класса Bomb (дочерний класс класса Projectile)"""
        super().__init__(x, y)

    def radius_up(self):
        """Метод увеличивает радиус бомбы."""
        self.r = self.r + 0.5
        return self.r

    def draw(self):
        """Метод отрисовывает положение бомбы на экране."""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        if self.vx < 1 and self.vy == 0 and self.r <= 40:
            self.r = self.radius_up()


class Gun:
    def __init__(self, gun_x, gun_y):
        """ Конструктор класса Gun

        Args:
        gun_x - начальное положение левого верхнего угла пушки по горизонтали
        gun_y - начальное положение левого верхнего угла пушки по вертикали
        """
        self.screen = screen
        self.f_power = 10
        self.f_on = 0
        self.an = 1
        self.color = GREY
        self.y = gun_y
        self.x = gun_x
        self.length = 30
        self.width = 10
        self.body_width = 30
        self.body_height = 30
        self.body_color = BLACK
        self.motion = "STOP"

    def fire_start(self):
        """Метод активирует пушку."""
        self.f_on = 1

    def fire1_end(self, event):
        """Выстрел из пушки бомбой.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        и времени нажатия на правую кнопку мыши.
        """
        new_bullet_bomb = Bomb(self.x, self.y)
        self.an = math.atan2((event.pos[1]-new_bullet_bomb.y), (event.pos[0]-new_bullet_bomb.x))
        new_bullet_bomb.vx = self.f_power * math.cos(self.an)
        new_bullet_bomb.vy = - self.f_power * math.sin(self.an)
        self.f_on = 0
        self.f_power = 10
        return new_bullet_bomb

    def fire2_end(self, event):
        """Выстрел из пушки пулей.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        и времени нажатия на правую кнопку мыши.
        """
        new_bullet = Bullet(self.x, self.y)
        self.an = math.atan2((event.pos[1]-new_bullet.y), (event.pos[0]-new_bullet.x))
        new_bullet.vx = self.f_power * math.cos(self.an)
        new_bullet.vy = - self.f_power * math.sin(self.an)
        self.f_on = 0
        self.f_power = 10
        return new_bullet

    def fire3_end(self, x, y, color):
        """Метод создаёт пулю из бомбы."""
        new_bullet_from_bomb = BulletFromBomb(x, y, color)
        return new_bullet_from_bomb

    def draw(self):
        """Метод отрисовывает положение положение пушки на экране."""
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        self.an = math.atan2((-y_mouse + self.y), (x_mouse - self.x))
        length_up = self.length + self.f_power
        width_half = self.width / 2
        pygame.draw.rect(self.screen, self.body_color, (self.x - self.body_width/2, self.y - self.body_height/2,
                                                        self.body_width, self.body_height))
        pygame.draw.polygon(self.screen, self.color, (
                           (self.x - width_half * math.sin(self.an),
                            self.y - width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an),
                            self.y + width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y + width_half * math.cos(self.an) - length_up * math.sin(self.an)),
                           (self.x - width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y - width_half * math.cos(self.an) - length_up * math.sin(self.an)))
                            )

    def power_up(self):
        """Метод удлинняет пушку, увеличивает начальную скорость пули при длительном нажатии на правую кнопку мыши."""
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = YELLOW
        else:
            self.color = GREY

    def check_move(self, event):
        """Метод перемещает пушку в зависимости от нажатой кнопки на клавиатуре."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.motion = "LEFT"
            elif event.key == pygame.K_RIGHT:
                self.motion = "RIGHT"
            elif event.key == pygame.K_UP:
                self.motion = "UP"
            elif event.key == pygame.K_DOWN:
                self.motion = "DOWN"
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                self.motion = "STOP"

    def move(self):
        if self.motion == "LEFT":
            self.x -= 3
        elif self.motion == "RIGHT":
            self.x += 3
        elif self.motion == "UP":
            self.y -= 3
        elif self.motion == "DOWN":
            self.y += 3

        if self.x - self.body_width/2 < 0:
            self.x = self.body_width/2
        if self.x + self.body_height/2 > WIDTH:
            self.x = WIDTH - self.body_width/2
        if self.y - self.body_height/2 < 0:
            self.y = self.body_height/2
        if self.y + self.body_height/2 >= HEIGHT:
            self.y = HEIGHT - self.body_height/2


class GunEnemy(Gun):
    def __init__(self, gun_x, gun_y):
        """ Конструктор класса GunEnemy дочернего класса для класса Gun

        Args:
        gun_x - начальное положение левого верхнего угла пушки по горизонтали
        gun_y - начальное положение левого верхнего угла пушки по вертикали
        """
        super().__init__(gun_x, gun_y)
        self.body_color = BLUE
        self.vy = randint(-2, 2)
        self.vx = randint(-2, 2)

    def check_distance(self, obj):
        """Метод проверяет расстояение от вражеской пушки до пушки игрока."""
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= 200**2:
            return True
        else:
            return False

    def draw_enemy(self, obj):
        """Метод отрисовывает положение положение пушки на экране."""
        x_mouse, y_mouse = obj.x, obj.y
        if self.check_distance(obj):
            self.an = math.atan2((-y_mouse + self.y), (x_mouse - self.x))
            self.color = YELLOW
        else:
            self.an = 0
            self.color = GREY
        length_up = self.length + self.f_power
        width_half = self.width / 2
        pygame.draw.rect(self.screen, self.body_color,
                         (self.x - self.body_width/2, self.y - self.body_height/2, self.body_width, self.body_height))
        pygame.draw.polygon(self.screen, self.color, (
                           (self.x - width_half * math.sin(self.an),
                            self.y - width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an),
                            self.y + width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y + width_half * math.cos(self.an) - length_up * math.sin(self.an)),
                           (self.x - width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y - width_half * math.cos(self.an) - length_up * math.sin(self.an)))
                            )

    def fire2_end_enemy(self, x, y):
        """Выстрел из пушки пулей.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        и времени нажатия на правую кнопку мыши.
        """
        new_bullet_enemy = BulletEnemy(self.x, self.y)
        self.an = math.atan2((y - new_bullet_enemy.y), (x - new_bullet_enemy.x))
        new_bullet_enemy.vx = self.f_power * math.cos(self.an)
        new_bullet_enemy.vy = - self.f_power * math.sin(self.an)
        self.f_on = 0
        self.f_power = 10
        return new_bullet_enemy

    def move_enemy(self):
        """Метод перемещает вражескую пушку с учётом отражениея от стен."""
        self.x += self.vx
        self.y += self.vy
        if self.x - self.body_width/2 < 0:
            self.vx = randint(1, 2)
        if self.x + self.body_width/2 > WIDTH:
            self.vx = randint(-2, -1)
        if self.y - self.body_height/2 < 0:
            self.vy = randint(1, 2)
        if self.y + self.body_height/2 > HEIGHT:
            self.vy = randint(-2, -1)


class BulletFromTarget(Projectile):
    def __init__(self, x, y):
        """Конструктор класса Bullet (дочерний класс класса Projectile)"""
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.vy = 0
        self.vx = 0
        self.color = BLACK


class Target:
    def __init__(self):
        """ Конструктор класса Target"""
        self.screen = screen
        self.x = randint(100, 700)
        self.y = randint(100, 500)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = RED


class TargetBall(Target):
    def __init__(self):
        """Конструктор класса TargetBall (дочерний класс класса Target)"""
        super().__init__()
        self.r = randint(20, 50)

    def move(self):
        """Метод перемещает цель.
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        отражения от стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy

        if self.x - self.r < 0:
            self.vx = randint(1, 10)
            self.x = self.r
        if self.x + self.r > WIDTH:
            self.vx = randint(-10, -1)
            self.x = WIDTH - self.r
        if self.y - self.r < 0:
            self.vy = randint(1, 10)
            self.y = self.r
        if self.y + self.r >= HEIGHT:
            self.vy = randint(-10, -1)
            self.y = HEIGHT - self.r

    def draw(self):
        """Метод отрисовывает цель на экране."""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class TargetRectangle(Target):
    def __init__(self):
        """Конструктор класса TargetRectangle (дочерний класс класса Target)"""
        super().__init__()
        self.width = randint(30, 100)
        self.height = randint(30, 100)

    def move(self):
        """Метод двигает прямоуголник (меняет координаты)
        Если прямоугольник ударился о стенку меняет скорость прямоугольника"""
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.vx = randint(1, 10)
            self.width -= 5
        if self.x + self.width > WIDTH:
            self.vx = randint(-10, -1)
            self.width -= 5
        if self.y < 0:
            self.vy = randint(1, 10)
            self.height -= 5
        if self.y + self.height > HEIGHT:
            self.vy = randint(-10, -1)
            self.height -= 5

    def draw(self):
        """Метод отрисовывает новое положение прямоугольника"""
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))


class Game:
    def __init__(self, rectangles_quantity=3, balls_quantity=3):
        """ Конструктор класса Gun
        Args:
        targets_quantity - количество целей.
        points - количество поражённых целей.
        """
        self.screen = screen
        self.bullets = []
        self.bullets_enemy = []
        self.bombs = []
        self.balls = []
        self.rectangles = []
        self.bombs_from_target = []
        self.balls_quantity = balls_quantity
        self.rectangles_quantity = rectangles_quantity
        self.gun = Gun(randint(100, WIDTH-100), randint(100, HEIGHT-100))
        self.gun_enemy = GunEnemy(randint(100, WIDTH-100), randint(100, HEIGHT-100))

    def collide_targets(self, target):
        """Метод изменяет движение целей в зависимости от их столкновения друг с другом."""
        for j in range(len(self.balls)-1):
            if (target.x-self.balls[j].x)**2+(target.y-self.balls[j].y)**2 < (target.r + self.balls[j].r)**2:
                if target.x > self.balls[j].x:
                    x = target.x
                    target.x += (self.balls[j].x +
                                 ((target.r + self.balls[j].r) ** 2 - (target.y - self.balls[j].y) ** 2) ** 0.5
                                 - target.x)/2
                    self.balls[j].x -= (self.balls[j].x - (x - (
                                         (target.r+self.balls[j].r)**2 - (target.y-self.balls[j].y)**2)**0.5))/2
                if target.x < self.balls[j].x:
                    x = target.x
                    target.x -= (target.x - (self.balls[j].x - (
                            (target.r+self.balls[j].r)**2 - (target.y-self.balls[j].y)**2) ** 0.5))/2
                    self.balls[j].x += (x + (
                            (target.r+self.balls[j].r)**2 - (target.y-self.balls[j].y)**2) ** 0.5
                                          - self.balls[j].x)/2
                if target.y > self.balls[j].y:
                    y = target.y
                    target.y += (self.balls[j].y +
                                 ((target.r + self.balls[j].r) ** 2 - (target.x - self.balls[j].x) ** 2) ** 0.5
                                 - target.y)/2
                    self.balls[j].y -= (self.balls[j].y - (y - (
                            (target.r+self.balls[j].r)**2 - (target.x-self.balls[j].x)**2)**0.5))/2
                if target.y < self.balls[j].y:
                    y = target.y
                    target.y -= (target.y - (self.balls[j].y - (
                            (target.r+self.balls[j].r)**2 - (target.x-self.balls[j].x)**2) ** 0.5))/2
                    self.balls[j].x += (y + (
                            (target.r+self.balls[j].r)**2 - (target.x-self.balls[j].x)**2) ** 0.5
                                          - self.balls[j].y)/2
                target.vx, self.balls[j].vx = self.balls[j].vx, target.vx
                target.vy, self.balls[j].vy = self.balls[j].vy, target.vy

    def check_len(self):
        global points
        for i in range(len(self.rectangles)):
            if self.rectangles[i].width <= 0 or self.rectangles[i].height <= 0:
                points -= 5
                self.rectangles.pop(i)
                self.rectangles.append(TargetRectangle())

    def draw_points(self):
        """Метод отрисовывает количество поражённых целей на экране."""
        text = FONT.render('Score: ' + str(points), True, BLACK)
        self.screen.blit(text, (WIDTH/3, 20))

    def custom_key(self, k):
        """Вспомогательный метод. Возвращает параметр, по которому следует проводить сортировку."""
        return k[1]

    def results_table(self):
        """Метод выводит результаты игры в файл GunResults в порядке убывания."""
        print('Enter your name: ')
        name = input()
        results = []
        with open("GunResults.txt", 'r') as output:
            records = output.readlines()

        if len(records) == 0:
            with open("GunResults.txt", 'w') as output:
                output.write(name + ": " + str(points) + '\n')
        else:
            names = list(map(lambda x: x.split(': ')[0], records))
            scores = list(map(lambda x: x.split(': ')[1], records))
            scores = list(map(lambda x: x.split('\n')[0], scores))
            for i in range(len(records)):
                results.append([names[i], int(scores[i])])
            results.append([name, points])
            results.sort(key=self.custom_key, reverse=True)
            output = open("GunResults.txt", 'w')
            for i in range(len(results)):
                output.write(str(results[i][0]) + ": " + str(results[i][1]) + '\n')
            output.close()

    def mainloop(self):
        """Метод описывает основной цикл игры."""
        global points
        for t1 in range(self.balls_quantity):  # создаём заданное колиество целей 1 и 2 типа (шары и прямоугольники)
            self.balls.append(TargetBall())
        for t2 in range(self.rectangles_quantity):
            self.rectangles.append(TargetRectangle())

        clock = pygame.time.Clock()
        finished = False

        while not finished:
            self.screen.fill(WHITE)
            self.gun.draw()
            self.gun_enemy.draw_enemy(self.gun)
            self.gun_enemy.move_enemy()

            for t1 in self.balls:  # осуществяем столкновение шариков
                t1.draw()
                self.collide_targets(t1)
                if abs(self.gun.x - t1.x) <= 1 and self.gun.y > t1.y and randint(0, 1) == 1:
                    self.bombs_from_target.append(BulletFromTarget(t1.x, t1.y))
                t1.move()

            for t2 in self.rectangles:  # отрисовываем положение прямоугольником и смещаем их
                t2.draw()
                t2.move()

            for bt in self.bombs_from_target:  # проверяем столкновение бомбочек, появляющихся из шариков-целей с пушкой
                bt.draw()
                bt.move()
                if bt.hittest(self.gun):
                    points -= 5
                    self.bombs_from_target.remove(bt)
                if bt.life() > 100:
                    self.bombs_from_target.remove(bt)

            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # производим выстрел пушкой
                    self.gun.fire_start()
                elif event.type == pygame.MOUSEBUTTONUP and (points % 5 != 0 or points == 0 or len(self.bombs) != 0):
                    new_bullet = self.gun.fire2_end(event)
                    self.bullets.append(new_bullet)
                elif event.type == pygame.MOUSEBUTTONUP and points % 5 == 0 and points != 0 and len(self.bombs) == 0:
                    new_bullet_bomb = self.gun.fire1_end(event)
                    self.bombs.append(new_bullet_bomb)
                self.gun.check_move(event)

            self.gun.move()

            if self.gun_enemy.check_distance(self.gun):  # выстрел вражеской пушки
                if randint(0, 100) == 1:
                    self.gun_enemy.fire_start()
                    for i in range(randint(30, 100)):
                        self.gun_enemy.power_up()
                    new_bullet_enemy = self.gun_enemy.fire2_end_enemy(self.gun.x, self.gun.y)
                    self.bullets_enemy.append(new_bullet_enemy)


            for b2 in self.bullets:  # изменяем положение и количество пуль в зависимости от попадания по целям
                b2.draw()
                b2.move()
                for t1 in range(len(self.balls)):
                    if b2.hittest(self.balls[t1]):
                        points += 1
                        self.bullets.remove(b2)
                        self.balls[t1] = TargetBall()
                for t2 in range(len(self.rectangles)):
                    if b2.hittest(self.rectangles[t2]):
                        points += 3
                        self.bullets.remove(b2)
                        self.rectangles[t2] = TargetRectangle()
                if b2.hittest(self.gun_enemy):
                    points += 20
                    self.bullets.remove(b2)
                if b2.life() > 150:
                    self.bullets.remove(b2)

            if len(self.bombs) != 0:  # если есть бомба изменяем её положение и создаём новые пули после её исчезновения
                for b1 in self.bombs:
                    b1.draw()
                    b1.move()
                    for t1 in range(len(self.balls)):
                        if b1.hittest(t1):
                            points += 1
                            self.balls[t1] = TargetBall()
                            for i in range(int(b1.r) // 5):
                                self.bullets.append(self.gun.fire3_end(b1.x, b1.y, b1.color))
                            self.bombs.remove(b1)
                    for t2 in range(len(self.rectangles)):
                        if b1.hittest(t2):
                            points += 3
                            self.rectangles[t2] = TargetRectangle()
                            for i in range(int(b1.r) // 5):
                                self.bullets.append(self.gun.fire3_end(b1.x, b1.y, b1.color))
                            self.bombs.remove(b1)
                    if b1.life() > 100:
                        for i in range(int(b1.r) // 5):
                            self.bullets.append(self.gun.fire3_end(b1.x, b1.y, b1.color))
                        self.bombs.remove(b1)

            for be in self.bullets_enemy:  # изменяем положение и количество пуль в зависимости от попадания в пушку
                be.draw()
                be.move()
                if be.hittest_bullet_enemy(self.gun):
                    points -= 20
                    self.bullets_enemy.remove(be)
                if be.life() > 150:
                    self.bullets_enemy.remove(be)

            self.check_len()  # проверяем, не сплющился ли до 0 прямоугольник-цель
            self.gun.power_up()  # перезаряжаем пушку
            self.draw_points()  # отрисовываем счёт на экране
            pygame.display.update()
        pygame.quit()
        self.results_table()  # экспортируем результаты игры в таблицу


def main():
    """Фунция запускает игру."""
    global screen
    global FONT
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT = pygame.font.SysFont('century gothic', 36)
    pygame.font.init()
    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
