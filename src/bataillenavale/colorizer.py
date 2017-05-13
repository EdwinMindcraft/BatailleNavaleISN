import pygame.surfarray


def create_invalid (surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = 255
    
def create_selected (surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,1] = 255