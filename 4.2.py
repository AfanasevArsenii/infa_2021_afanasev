import pygame
from pygame.draw import *
import math


pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 600))
screen.fill((240, 255, 255))

tent = pygame.Surface((300, 300), pygame.SRCALPHA)


man = pygame.Surface((200, 200), pygame.SRCALPHA)
coat = pygame.Surface.subsurface(man, (50, 40, 100, 100))
left_arm = pygame.Surface.subsurface(man, (20, 70, 60, 15))
right_arm = pygame.Surface.subsurface(man, (120, 70, 60, 15))

cat = pygame.Surface((200, 200), pygame.SRCALPHA)
fish = pygame.Surface.subsurface(cat, (20,20))


rect(screen, (255, 255, 240), (0, 0, 400, 250))

circle(screen, (230, 230, 250), (130, 300), 100, draw_top_right = True, draw_top_left = True)
arc(screen, (25, 25, 112), (30, 190, 200, 250), 0, math.pi, 3)
arc(screen, (25, 25, 112), (30, 255, 200, 100), math.pi, 2*math.pi, 3)
arc(screen, (25, 25, 112), (40, 210, 180, 100), math.pi, 2*math.pi, 3)
arc(screen, (25, 25, 112), (60, 180, 140, 90), math.pi, 2*math.pi, 3)
arc(screen, (25, 25, 112), (85, 170, 90, 60), math.pi, 2*math.pi, 3)
arc(screen, (25, 25, 112), (100, 200, 80, 290), 0, math.pi/2, 3)
arc(screen, (25, 25, 112), (80, 200, 80, 300), math.pi/2, math.pi,  3)
ellipse(screen, (25, 25, 112), (115, 195, 30, 10), 3)



ellipse(coat, (205, 170, 125), (5, 0, 90, 200), 0) # куртка основа
rect(coat, (255, 211, 155), (0, 80, 100, 20), border_radius=5)
rect(coat, (255, 211, 155), (45, 0, 10, 90), border_radius=5)

ellipse(man, (255, 211, 155), (60, 1, 80, 70), 0) # капюшон пух
ellipse(man, (205, 170, 125), (65, 10, 70, 60), 0) # капюшон
ellipse(man, (255, 255, 224), (75, 20, 50, 40), 0) # лицо

#левая рука
ellipse(left_arm, (205, 170, 125), (0, 0, 60, 15), 0)
left_arm = pygame.transform.rotate(left_arm, -30)
man.blit(left_arm, (15, 45))
#правая рука
ellipse(right_arm, (205, 170, 125), (0, 0, 60, 15), 0)
right_arm = pygame.transform.rotate(right_arm, -30)
right_arm = pygame.transform.scale(right_arm, (120, 30))
# левый валенок
rect(man, (205, 170, 125), (75, 135, 20, 30), border_radius=5)
rect(man, (205, 170, 125), (105, 145, 30, 20), border_radius=10)
# правый валенок
rect(man, (205, 170, 125), (105, 135, 20, 30), border_radius=5)
rect(man, (205, 170, 125), (65, 145, 20, 20), border_radius=10)

# удочка
line(man, (0, 0, 0), (30,40), (20, 160), 2)

#кошка



pygame.Surface.unlock(man)
pygame.Surface.unlock(coat)
screen.blit(man, (200, 350))



#pygame.transform.flip(surf, True, False)



pygame.display.update()

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()