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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

global screen, FONT


class Bullet:
    def __init__(self, x=40, y=450):
        """ Конструктор класса Bullet

        Args:
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.ay = 10
        self.lifetime = 0

    def life(self):
        """Функция подсчитывает, сколько времени живёт пуля."""
        self.lifetime += 1
        return self.lifetime

    def move(self):
        """Функция перемещает пулю.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на пулю,
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

    def draw(self):
        """Функиця отрисовывает положение пули на экране."""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли пуля с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, x=40, y=450):
        """ Конструктор класса Gun

        Args:
        x - начальное положение левого верхнего угла пушки по горизонтали
        y - начальное положение левого верхнего угла пушки по вертикали
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.y = y
        self.x = x
        self.length = 30
        self.width = 10

    def fire2_start(self):
        """Функция активирует пушку."""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел из пушки пулей.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши
        и времени нажатия на правую кнопку мыши.
        """
        new_bullet = Bullet()
        self.an = math.atan2((event.pos[1]-new_bullet.y), (event.pos[0]-new_bullet.x))
        new_bullet.vx = self.f2_power * math.cos(self.an)
        new_bullet.vy = - self.f2_power * math.sin(self.an)
        self.f2_on = 0
        self.f2_power = 10
        return new_bullet

    def draw(self):
        """Функция отрисовывает положение положение пушки на экране."""
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        self.an = math.atan2((-y_mouse + self.y), (x_mouse - self.x))
        length_up = self.length + self.f2_power
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
        """Функция удлинняет пушку, увеличивает начальную скорость пули при длительном нажатии на правую кнопку мыши."""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """ Конструктор класса Target"""
        self.screen = screen
        self.points = 0
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(20, 50)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.color = RED

    def move(self):
        """Функция перемещает цель.

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
        """Функция отрисовывает цель на экране."""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Game:
    def __init__(self, targets_quantity=5, points=0):
        """ Конструктор класса Gun

        Args:
        targets_quantity - количество целей.
        points - количество поражённых целей.
        """
        self.screen = screen
        self.bullets = []
        self.targets = []
        self.targets_quantity = targets_quantity
        self.gun = Gun()
        self.points = points

    def collide_targets(self, target):
        """Функция изменяет движение целей в зависимости от их столкновения друг с другом."""
        for j in range(len(self.targets)-1):
            if (target.x-self.targets[j].x)**2+(target.y-self.targets[j].y)**2 < (target.r + self.targets[j].r)**2:
                if target.x > self.targets[j].x:
                    x =target.x
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
        """Функция отрисовывает количество поражённых целей на экране."""
        text = FONT.render('Score: ' + str(self.points), True, BLACK)
        self.screen.blit(text, (WIDTH/3, 20))

    def custom_key(self, k):
        """Вспомогательная функция. Возвращает параметр, по которому следует проводить сортировку."""
        return k[1]

    def results_table(self):
        """Функция выводит результаты игры в файл GunResults в порядке убывания."""
        print('Enter your name: ')
        name = input()
        results = []
        with open("GunResults.txt", 'r') as output:
            records = output.readlines()

        if len(records) == 0:
            with open("GunResults.txt", 'w') as output:
                output.write(name + ": " + str(self.points) + '\n')
        else:
            names = list(map(lambda x: x.split(': ')[0], records))
            scores = list(map(lambda x: x.split(': ')[1], records))
            scores = list(map(lambda x: x.split('\n')[0], scores))
            for i in range(len(records)):
                results.append([names[i], int(scores[i])])
            results.append([name, self.points])
            results.sort(key=self.custom_key, reverse=True)
            output = open("GunResults.txt", 'w')
            for i in range(len(results)):
                output.write(str(results[i][0]) + ": " + str(results[i][1]) + '\n')
            output.close()

    def mainloop(self):
        """Функция описывает основной цикл игры."""
        for t in range(self.targets_quantity):
            self.targets.append(Target())

        clock = pygame.time.Clock()
        finished = False

        while not finished:
            self.screen.fill(WHITE)
            self.gun.draw()

            for b in self.bullets:
                b.draw()

            for t in range(len(self.targets)):
                self.targets[t].move()
                self.collide_targets(self.targets[t])
                self.targets[t].draw()

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_bullet = self.gun.fire2_end(event)
                    self.bullets.append(new_bullet)

            for b in self.bullets:
                b.move()
                for t in range(len(self.targets)):
                    if b.hittest(self.targets[t]):
                        self.points += 1
                        self.targets[t] = Target()
                        self.bullets.remove(b)
                if b.life() > 150:
                    self.bullets.remove(b)
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
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT = pygame.font.SysFont('century gothic', 36)
    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
