import pygame
from pygame.draw import *
import math


pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 800))
screen.fill((240, 255, 255))

tent = pygame.Surface((300, 300), pygame.SRCALPHA)
tent_color_up = pygame.Surface.subsurface(tent, (0, 100, 200, 120))
tent_color_down = pygame.Surface.subsurface(tent, (0, 165, 200, 100))

man = pygame.Surface((200, 200), pygame.SRCALPHA)
coat = pygame.Surface.subsurface(man, (50, 40, 100, 100))
left_arm = pygame.Surface((60, 15), pygame.SRCALPHA)
right_arm = pygame.Surface((60, 15), pygame.SRCALPHA)

cat = pygame.Surface((200, 200), pygame.SRCALPHA)
cat_left_arm = pygame.Surface((60, 15), pygame.SRCALPHA)
cat_right_arm = pygame.Surface((60, 15), pygame.SRCALPHA)
cat_left_leg = pygame.Surface((60, 15), pygame.SRCALPHA)
cat_right_leg = pygame.Surface((60, 15), pygame.SRCALPHA)
cat_tail = pygame.Surface((80, 20), pygame.SRCALPHA)
fish = pygame.Surface((100, 100), pygame.SRCALPHA)


rect(screen, (255, 255, 240), (0, 0, 1200, 300))

def draw_tent(tent, x, y, k, p, color):
    ellipse(tent_color_up, color, (0, 0, 200, 250))
    ellipse(tent_color_down, color, (0, 0, 200, 100))
    arc(tent, (25, 25, 112), (0, 100, 200, 250), 0, math.pi, 3)
    arc(tent, (25, 25, 112), (0, 165, 200, 100), math.pi, 2*math.pi, 3)
    arc(tent, (25, 25, 112), (10, 120, 180, 100), math.pi, 2*math.pi, 3)
    arc(tent, (25, 25, 112), (30, 90, 140, 90), math.pi, 2*math.pi, 3)
    arc(tent, (25, 25, 112), (55, 80, 90, 60), math.pi, 2*math.pi, 3)
    arc(tent, (25, 25, 112), (70, 110, 80, 290), 0, math.pi/2, 3)
    arc(tent, (25, 25, 112), (50, 110, 80, 300), math.pi/2, math.pi,  3)
    ellipse(tent, (25, 25, 112), (85, 105, 30, 10), 3)
    tent.set_alpha(p)
    tent = pygame.transform.scale(tent, (300*k, 300*k))
    screen.blit(tent, (x, y))


def draw_man(man, left_arm, right_arm, x, y, k, p, color_coat, color_fluff, color_face, color_shoe):

    ellipse(coat, color_coat, (5, 0, 90, 200), 0) # куртка основа
    rect(coat, color_fluff, (0, 80, 100, 20), border_radius=5)
    rect(coat, color_fluff, (45, 0, 10, 90), border_radius=5)

    ellipse(man, color_fluff, (60, 1, 80, 70), 0)  # капюшон пух
    ellipse(man, color_coat, (65, 10, 70, 60), 0)  # капюшон
    ellipse(man, color_face, (75, 20, 50, 40), 0)  # лицо
    line(man, (0, 0, 0), (95, 35), (85, 30), 2)  # левый глаз
    line(man, (0, 0, 0), (105, 35), (115, 30), 2)  # правый глаз
    arc(man, (0, 0, 0), (93, 45, 15, 10), 0, math.pi, 2)  # рот
    # левая рука
    ellipse(left_arm, color_coat, (0, 0, 60, 15), 0)
    left_arm = pygame.transform.rotate(left_arm, -40)
    man.blit(left_arm, (25, 35))
    # правая рука
    ellipse(right_arm, color_coat, (0, 0, 60, 15), 0)
    right_arm = pygame.transform.rotate(right_arm, -30)
    man.blit(right_arm, (120, 60))
    # левый валенок
    rect(man, color_shoe, (75, 135, 20, 30), border_radius=5)
    rect(man, color_shoe, (105, 145, 30, 20), border_radius=10)
    # правый валенок
    rect(man, color_shoe, (105, 135, 20, 30), border_radius=5)
    rect(man, color_shoe, (65, 145, 20, 20), border_radius=10)
    # удочка
    line(man, (0, 0, 0), (30, 40), (20, 160), 2)
    man.set_alpha(p)
    man = pygame.transform.scale(man, (200*k, 200*k))
    screen.blit(man, (x, y))


def draw_cat(cat, cat_left_arm, cat_right_arm, cat_left_leg, cat_right_leg, cat_tail, fish,  x, y, color_cat, k, p, yflip):
    # кошка
    ellipse(cat, color_cat, (60, 70, 90, 30))  # тело
    ellipse(cat, color_cat, (45, 51, 35, 30))  # голова
    ellipse(cat, (255, 255, 255), (50, 60, 10, 5))  # левый глаз
    ellipse(cat, (255, 255, 255), (65, 60, 10, 5))  # правый глаз
    ellipse(cat, (0, 0, 0), (50, 60, 5, 5))  # левый зрачок
    ellipse(cat, (0, 0, 0), (65, 60, 5, 5))  # правый зрачок
    polygon(cat, color_cat, [(50, 60), (60, 50), (45, 45)])  # левое ухо
    polygon(cat, color_cat, [(80, 65), (80, 45), (65, 50)])  # левое ухо
    ellipse(cat, (0, 0, 0), (58, 67, 5, 5))

    ellipse(cat_left_arm, (255, 130, 71), (0, 0, 60, 15))
    cat_left_arm = pygame.transform.rotate(cat_left_arm, 30)
    cat.blit(cat_left_arm, (15, 80))
    ellipse(cat_right_arm, (255, 130, 71), (0, 0, 60, 15))
    cat_right_arm = pygame.transform.rotate(cat_right_arm, 50)
    cat.blit(cat_right_arm, (40, 80))

    ellipse(cat_left_leg, (255, 130, 71), (0, 0, 60, 15))
    cat_left_leg = pygame.transform.rotate(cat_left_leg, -60)
    cat.blit(cat_left_leg, (120, 80))

    ellipse(cat_right_leg, (255, 130, 71), (0, 0, 60, 15))
    cat_right_leg = pygame.transform.rotate(cat_right_leg, -30)
    cat.blit(cat_right_leg, (130, 80))

    ellipse(cat_tail, (255, 130, 71), (0, 0, 80, 20))
    cat_tail = pygame.transform.rotate(cat_tail, 230)
    cat.blit(cat_tail, (130, 25))

    ellipse(fish, (102, 205, 170), (0, 0, 40, 10))
    polygon(fish, (178, 34, 34), [(40, 5), (50, 10), (35, 15)])
    fish = pygame.transform.rotate(fish, -20)
    cat.blit(fish, (0, 65))

    cat = pygame.transform.scale(man, (200*k, 200*k))
    cat = pygame.transform.flip(cat, False, yflip)
    cat.set_alpha(p)
    screen.blit(cat, (x, y))


draw_tent(tent, 100, 100, 1, 255, (224, 255, 255))
draw_man(man, left_arm, right_arm, 300, 300, 1, 255, (205, 170, 125), (255, 211, 155), (255, 255, 224), (205, 170, 125))
draw_cat(cat, cat_left_arm, cat_right_arm, cat_left_leg, cat_right_leg, cat_tail, fish,  200, 400, (255, 130, 71), 1, 255, False)

pygame.display.update()

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()