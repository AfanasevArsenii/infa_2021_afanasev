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


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
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

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vy -= self.ay
        self.x += self.vx
        self.y -= self.vy
        """if (self.x - self.r < 0 and self.vx < 0) or (self.x + self.r > 800 and self.vx > 0):
            self.vx = - self.vx
        if ((self.y - self.r < 0) and (self.vy > 0)) or ((self.y + self.r > 600) and (self.vy < 0)):
            self.vy = -self.vy
            if abs(self.vy) < 1:
                self.vx = 0
                self.vy = 0
                self.ay = 0"""
        if self.x - self.r < 0:
            self.vx = - self.vx
            self.x = self.r
        if self.x + self.r > 800:
            self.vx = - self.vx
            self.x = 800 - self.r
        if self.y - self.r < 0:
            self.vy = -self.vy
            self.y = self.r
        if self.y + self.r >= 600:
            self.vy = -0.9*self.vy
            self.y = 600 - self.r
            print(self.vx, self.vy)
            if abs(self.vy) < 5:
                self.vx = 0
                self.vy = 0
                self.ay = 0
                print(self.vx, self.vy, self.ay)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        self.f2_on = 0
        self.f2_power = 10
        return new_ball


    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        pass


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        '''Инициализация новой цели.'''
        self.screen = screen
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?


        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.balls = []
        self.bullet = 0
        self.gun = Gun(screen)
        self.target = Target(screen)

    def mainloop(self):
        clock = pygame.time.Clock()
        finished = False

        while not finished:
            self.screen.fill(WHITE)
            self.gun.draw()
            self.target.draw()
            for b in self.balls:
                b.draw()
            pygame.display.update()

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_ball = self.gun.fire2_end(event)
                    self.bullet += 1
                    self.balls.append(new_ball)
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)

            for b in self.balls:
                b.move()
                if b.hittest(self.target) and self.target.live:
                    self.target.live = 0
                    self.target.hit()
                    self.target.new_target()
            self.gun.power_up()

        pygame.quit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen)
    game.mainloop()
if __name__ == '__main__':
    main()
