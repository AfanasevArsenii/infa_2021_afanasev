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

global screen


class Ball:
    def __init__(self, x=40, y=450):
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
        # FIXME %%%
        self.vy -= self.ay
        self.x += self.vx
        self.y -= self.vy

        if self.x - self.r < 0:
            self.vx = - self.vx
            self.x = self.r
        if self.x + self.r > WIDTH:
            self.vx = - self.vx
            self.x = 800 - self.r
        if self.y - self.r < 0:
            self.vy = -self.vy
            self.y = self.r
        if self.y + self.r >= HEIGHT:
            self.vy = -0.9*self.vy
            self.y = 600 - self.r
            #print(self.vx, self.vy)
            if abs(self.vy) < 5:
                self.vx = 0
                self.vy = 0
                self.ay = 0
                #print(self.vx, self.vy, self.ay)

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
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, x=40, y=450):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.y = y
        self.x = x
        self.length = 30
        self.width = 10

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball()
        #new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        self.f2_on = 0
        self.f2_power = 10
        return new_ball

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        #if event:
            #self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        """if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY"""

    def draw(self):
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        self.an = math.atan2((-y_mouse + self.y), (x_mouse - self.x))
        #print(self.an)
        length_up = self.length + self.f2_power
        width_half = self.width / 2
        pygame.draw.polygon(self.screen, self.color, ((self.x - width_half * math.sin(self.an),
                                                       self.y - width_half * math.cos(self.an)),
                                                      (self.x + width_half * math.sin(self.an),
                                                       self.y + width_half * math.cos(self.an)),
                                                      (self.x + width_half * math.sin(self.an) + length_up * math.cos(self.an),
                                                       self.y + width_half * math.cos(self.an) - length_up * math.sin(self.an)),
                                                      (self.x - width_half * math.sin(self.an) + length_up * math.cos(self.an),
                                                       self.y - width_half * math.cos(self.an) - length_up * math.sin(self.an))))
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """Инициализация новой цели."""
        self.screen = screen
        self.points = 0
        self.live = 1

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
    def __init__(self):
        self.screen = screen
        self.balls = []
        self.bullet = 0
        self.gun = Gun()
        self.target = Target()

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
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game()
    game.mainloop()
if __name__ == '__main__':
    main()
