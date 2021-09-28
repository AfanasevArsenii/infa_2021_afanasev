import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((100,100,100))


circle(screen, (238, 232, 170), (200, 200), 150) #face
circle(screen, (178, 34, 34), (250, 160), 30) #right eye
circle(screen, (0,0,0), (250, 160), 15)
circle(screen, (178, 34, 34), (140, 170), 40) #left eye
circle(screen, (0, 0, 0), (140, 170), 20)

polygon(screen, (0, 0, 0), [(70, 60), (60, 70), (180,140), (190, 130)]) #left eyebrow
polygon(screen, (0, 0, 0), [(330, 80), (310, 110), (220,130), (220, 120)]) #right eyebrow
rect(screen, (0, 0, 0), (130, 270, 150, 10))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()