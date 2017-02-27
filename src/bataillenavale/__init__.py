import pygame
from pygame.constants import *

pygame.init()

window = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Bataille Navale")

should_close = False

bg = pygame.image.load("mer.jpg").convert()
bg = pygame.transform.scale(bg, window.get_size())
window.blit(bg, (0, 0))

while not should_close:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            should_close = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            print ("Ka")
    continue