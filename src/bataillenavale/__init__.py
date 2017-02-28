import pygame
from pygame.constants import *

grid_size = 400

pygame.init()

window = pygame.display.set_mode((grid_size * 2, grid_size))
pygame.display.set_caption("Bataille Navale")
pygame.display.set_icon(pygame.image.load("bato.jpg"))
should_close = False

bg = pygame.image.load("mer.jpg").convert()
bg = pygame.transform.scale(bg, window.get_size())

#carrier = pygame.image.load("carrier.jpg").convert_alpha()
#carrier = pygame.transform.scale(carrier, (200, 40))

while not should_close:
    window.blit(bg, (0, 0))
    #window.blit(carrier, (0, 40))
    for event in pygame.event.get():
        if event.type == QUIT:
            should_close = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            print ("Missed")
    
    pygame.display.flip() 

