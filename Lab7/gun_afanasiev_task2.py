import math
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
    def __init__(self):
        """ Конструктор класса Projectile снарядов.

        Args:
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        self.screen = screen
        self.x = 40
        self.y = 450
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.ay = 10
        self.lifetime = 0

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
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False


class Bullet(Projectile):
    def __init__(self):
        """Конструктор класса Bullet (дочерний класс класса Projectile)"""
        super().__init__()


class BulletFromBomb(Projectile):
    def __init__(self, x, y, color):
        """Конструктор класса BulletFromBomb (дочерний класс класса Projectile),
        создаёт пули(на месте бомбы с цветом бомбы со случайными скоростями),
        которые появляются после исчезновения бомбы или в случае попадания бомбой в цель."""
        super().__init__()
        self.x = x
        self.y = y
        self.r = 10
        self.vx = randint(-100, 100)
        self.vy = randint(-100, 100)
        self.color = color


class Bomb(Projectile):
    def __init__(self):
        """Конструктор класса Bomb (дочерний класс класса Projectile)"""
        super().__init__()

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
    def __init__(self, x=40, y=450):
        """ Конструктор класса Gun

        Args:
        x - начальное положение левого верхнего угла пушки по горизонтали
        y - начальное положение левого верхнего угла пушки по вертикали
        """
        self.screen = screen
        self.f_power = 10
        self.f_on = 0
        self.an = 1
        self.color = GREY
        self.y = y
        self.x = x
        self.length = 30
        self.width = 10

    def fire_start(self):
        """Метод активирует пушку."""
        self.f_on = 1

    def fire1_end(self, event):
        """Выстрел из пушки бомбой.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        и времени нажатия на правую кнопку мыши.
        """
        new_bullet_bomb = Bomb()
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
        new_bullet = Bullet()
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
        pygame.draw.polygon(self.screen, self.color,
                          ((self.x - width_half * math.sin(self.an),
                            self.y - width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an),
                            self.y + width_half * math.cos(self.an)),
                           (self.x + width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y + width_half * math.cos(self.an) - length_up * math.sin(self.an)),
                           (self.x - width_half * math.sin(self.an) + length_up * math.cos(self.an),
                            self.y - width_half * math.cos(self.an) - length_up * math.sin(self.an))))

    def power_up(self):
        """Метод удлинняет пушку, увеличивает начальную скорость пули при длительном нажатии на правую кнопку мыши."""
        if self.f_on:
            if self.f_power < 100:
                self.f_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """ Конструктор класса Target"""
        self.screen = screen
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(20, 50)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = RED

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
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Game:
    def __init__(self, targets_quantity=5):
        """ Конструктор класса Gun

        Args:
        targets_quantity - количество целей.
        points - количество поражённых целей.
        """
        self.screen = screen
        self.bullets = []
        self.bombs = []
        self.targets = []
        self.targets_quantity = targets_quantity
        self.gun = Gun()

    def collide_targets(self, target):
        """Метод изменяет движение целей в зависимости от их столкновения друг с другом."""
        for j in range(len(self.targets)-1):
            if (target.x-self.targets[j].x)**2+(target.y-self.targets[j].y)**2 < (target.r + self.targets[j].r)**2:
                if target.x > self.targets[j].x:
                    x = target.x
                    target.x += (self.targets[j].x +
                                 ((target.r + self.targets[j].r) ** 2 - (target.y - self.targets[j].y) ** 2) ** 0.5
                                 - target.x)/2
                    self.targets[j].x -= (self.targets[j].x - (x -
                                         ((target.r+self.targets[j].r)**2 - (target.y-self.targets[j].y)**2)**0.5))/2
                if target.x < self.targets[j].x:
                    x = target.x
                    target.x -= (target.x - (self.targets[j].x -
                                ((target.r+self.targets[j].r)**2 - (target.y-self.targets[j].y)**2) ** 0.5))/2
                    self.targets[j].x += (x +
                                          ((target.r+self.targets[j].r)**2 - (target.y-self.targets[j].y)**2) ** 0.5
                                          - self.targets[j].x)/2
                if target.y > self.targets[j].y:
                    y = target.y
                    target.y += (self.targets[j].y +
                                 ((target.r + self.targets[j].r) ** 2 - (target.x - self.targets[j].x) ** 2) ** 0.5
                                 - target.y)/2
                    self.targets[j].y -= (self.targets[j].y - (y -
                                         ((target.r+self.targets[j].r)**2 - (target.x-self.targets[j].x)**2)**0.5))/2
                if target.y < self.targets[j].y:
                    y = target.y
                    target.y -= (target.y - (self.targets[j].y -
                                ((target.r+self.targets[j].r)**2 - (target.x-self.targets[j].x)**2) ** 0.5))/2
                    self.targets[j].x += (y +
                                          ((target.r+self.targets[j].r)**2 - (target.x-self.targets[j].x)**2) ** 0.5
                                          - self.targets[j].y)/2
                target.vx, self.targets[j].vx = self.targets[j].vx, target.vx
                target.vy, self.targets[j].vy = self.targets[j].vy, target.vy

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
        for t in range(self.targets_quantity):
            self.targets.append(Target())

        clock = pygame.time.Clock()
        finished = False

        while not finished:
            self.screen.fill(WHITE)
            self.gun.draw()

            for t in range(len(self.targets)):
                self.targets[t].move()
                self.collide_targets(self.targets[t])
                self.targets[t].draw()

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire_start()
                elif event.type == pygame.MOUSEBUTTONUP and (points % 5 != 0 or points == 0 or len(self.bombs) != 0):
                    new_bullet = self.gun.fire2_end(event)
                    self.bullets.append(new_bullet)
                elif event.type == pygame.MOUSEBUTTONUP and points % 5 == 0 and points != 0 and len(self.bombs) == 0:
                    new_bullet_bomb = self.gun.fire1_end(event)
                    self.bombs.append(new_bullet_bomb)

            for b2 in self.bullets:  # изменяем положение и количество пуль
                b2.draw()
                b2.move()
                for t in range(len(self.targets)):
                    if b2.hittest(self.targets[t]):
                        points += 1
                        self.targets[t] = Target()
                        self.bullets.remove(b2)
                if b2.life() > 150:
                    self.bullets.remove(b2)

            if len(self.bombs) != 0:  # есть есть бомба изменяем её положение и создаём новые пули после её исчезновения
                for b1 in self.bombs:
                    b1.draw()
                    b1.move()
                    for t in range(len(self.targets)):
                        if b1.hittest(self.targets[t]):
                            points += 1
                            self.targets[t] = Target()
                            for i in range(int(b1.r) // 5):
                                self.bullets.append(self.gun.fire3_end(b1.x, b1.y, b1.color))
                            self.bombs.remove(b1)
                    if b1.life() > 100:
                        for i in range(int(b1.r) // 5):
                            self.bullets.append(self.gun.fire3_end(b1.x, b1.y, b1.color))
                        self.bombs.remove(b1)

            self.gun.power_up()
            self.draw_points()
            pygame.display.update()
        pygame.quit()
        self.results_table()


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
