import pygame
from pygame.constants import *
from bataillenavale import game
from bataillenavale import engine

render_offset = (10, 10)

grid_size = 500
pygame.init()
instance = game.Game(grid_size)

grid_size = instance.cube_size() * 11
instance.set_grid_size(grid_size)

window = pygame.display.set_mode((render_offset[0] * 4 + grid_size * 2, render_offset[1] * 2 + grid_size))
pygame.display.set_caption("Bataille Navale")
pygame.display.set_icon(pygame.image.load("bato.jpg"))
should_close = False

bg = pygame.image.load("mer.jpg").convert()
bg = pygame.transform.scale(bg, window.get_size())


line_vert = pygame.surface.Surface((1, instance.cube_size() * 11))
line_hori = pygame.surface.Surface((instance.cube_size() * 11, 1))

while not should_close:
    window.blit(bg, (0, 0))
    for i in range(0, grid_size + 1, instance.cube_size()):
        window.blit(line_vert, (render_offset[0] + i, render_offset[1]))
        window.blit(line_hori, (render_offset[0], render_offset[1] + i))
        
        window.blit(line_vert, (render_offset[0] * 3 + grid_size + i, render_offset[1]))
        window.blit(line_hori, (render_offset[0] * 3 + grid_size, render_offset[1] + i))
    for event in pygame.event.get():
        if event.type == QUIT:
            should_close = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            print ("Missed")
    
    pygame.display.flip() 



#carrier = pygame.image.load("carrier.jpg").convert_alpha()
#carrier = pygame.transform.scale(carrier, (200, 40))
