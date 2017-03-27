import pygame


def create_invalid (surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = 255

def create_transparent (surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,3] = 255