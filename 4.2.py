import pygame
from pygame.draw import *
import math


pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 600))
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


rect(screen, (255, 255, 240), (0, 0, 400, 250))


#circle(screen, (230, 230, 250), (130, 300), 100, draw_top_right = True, draw_top_left = True)
ellipse(tent_color_up, (224, 255, 255), (0, 0, 200, 250))
ellipse(tent_color_down, (224, 255, 255), (0, 0, 200, 100))
arc(tent, (25, 25, 112), (0, 100, 200, 250), 0, math.pi, 3)
arc(tent, (25, 25, 112), (0, 165, 200, 100), math.pi, 2*math.pi, 3)
arc(tent, (25, 25, 112), (10, 120, 180, 100), math.pi, 2*math.pi, 3)
arc(tent, (25, 25, 112), (30, 90, 140, 90), math.pi, 2*math.pi, 3)
arc(tent, (25, 25, 112), (55, 80, 90, 60), math.pi, 2*math.pi, 3)
arc(tent, (25, 25, 112), (70, 110, 80, 290), 0, math.pi/2, 3)
arc(tent, (25, 25, 112), (50, 110, 80, 300), math.pi/2, math.pi,  3)
ellipse(tent, (25, 25, 112), (85, 105, 30, 10), 3)



ellipse(coat, (205, 170, 125), (5, 0, 90, 200), 0) # куртка основа
rect(coat, (255, 211, 155), (0, 80, 100, 20), border_radius=5)
rect(coat, (255, 211, 155), (45, 0, 10, 90), border_radius=5)

ellipse(man, (255, 211, 155), (60, 1, 80, 70), 0) # капюшон пух
ellipse(man, (205, 170, 125), (65, 10, 70, 60), 0) # капюшон
ellipse(man, (255, 255, 224), (75, 20, 50, 40), 0) # лицо
line(man, (0, 0, 0), (95, 35), (85, 30), 2) # левый глаз
line(man, (0, 0, 0), (105, 35), (115, 30), 2) # правый глаз
arc(man, (0, 0, 0), (93, 45, 15, 10), 0, math.pi, 2) #рот
#левая рука
ellipse(left_arm, (205, 170, 125), (0, 0, 60, 15), 0)
left_arm = pygame.transform.rotate(left_arm, -40)
man.blit(left_arm, (25, 35))
#правая рука
ellipse(right_arm, (205, 170, 125), (0, 0, 60, 15), 0)
right_arm = pygame.transform.rotate(right_arm, -30)
man.blit(right_arm, (120, 60))
# левый валенок
rect(man, (205, 170, 125), (75, 135, 20, 30), border_radius=5)
rect(man, (205, 170, 125), (105, 145, 30, 20), border_radius=10)
# правый валенок
rect(man, (205, 170, 125), (105, 135, 20, 30), border_radius=5)
rect(man, (205, 170, 125), (65, 145, 20, 20), border_radius=10)

# удочка
line(man, (0, 0, 0), (30,40), (20, 160), 2)

#кошка
ellipse(cat, (255, 130, 71), (60, 70, 90, 30)) #тело
ellipse(cat, (255, 130, 71), (45, 51, 35, 30)) #голова
ellipse(cat, (255, 255, 255), (50, 60, 10, 5)) #левый глаз
ellipse(cat, (255, 255, 255), (65, 60, 10, 5)) #правый глаз
ellipse(cat, (0, 0, 0), (50, 60, 5, 5)) #левый глаз
ellipse(cat, (0, 0, 0), (65, 60, 5, 5)) #правый глаз
polygon(cat, (255, 130, 71), [(50, 60), (60, 50), (45, 45)]) #левое ухо
polygon(cat, (255, 130, 71), [(80, 65), (80, 45), (65, 50)]) #левое ухо
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

polygon(fish, (178, 34, 34), [(40, 10), (60, 0), (50, 20)])
polygon(fish, (178, 34, 34), [(10, 13), (40, 23), (30, 13)])
ellipse(fish, (102, 205, 170), (0, 5, 40, 10))
circle(fish, (0, 0, 0), (10,10), 1, 0)
polygon(fish, (255, 255, 255), [(30, 2), (27, 2), (28, 6)])
polygon(fish, (255, 255, 255), [(23, 2), (20, 2), (22, 6)])
fish = pygame.transform.rotate(fish, -20)
cat.blit(fish, (0, 65))

pygame.Surface.unlock(man)
pygame.Surface.unlock(coat)
pygame.Surface.unlock(cat)
screen.blit(man, (200, 310))

screen.blit(tent, (30, 70))
screen.blit(cat, (20, 430))



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