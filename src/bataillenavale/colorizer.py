import pygame


def create_invalid (surface):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = 255