import pygame
from pygame.draw import *
FPS = 30
screen = pygame.display.set_mode((400, 400))
right_arm = pygame.Surface((200, 200))
ellipse(right_arm, (205, 170, 125), (0, 0, 60, 15), 0)
right_arm = pygame.transform.rotate(right_arm, -30)

screen.blit(right_arm, (0, 0))

pygame.display.update()

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()