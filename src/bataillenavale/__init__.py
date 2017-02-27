import pygame
from pygame.locals import *


pygame.init()
window = pygame.display.set_mode((400, 400), RESIZABLE)

should_close = False

bg = pygame.image.load("mer.jpg").convert()
window.blit(bg, (0, 0))

while not should_close:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            should_close = True
    continue