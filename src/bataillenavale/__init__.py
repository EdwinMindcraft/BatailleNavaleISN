import pygame
from pygame.constants import *
from bataillenavale import game
from bataillenavale import engine

render_offset = (10, 10)

#Ordre de taille de la grille.
grid_size = 500
#Initialisation de pygame
pygame.init()

#Regles
rules = engine.Rules()

#Creation de l'instance du jeu
instance = game.Game(grid_size, rules=rules)

#Calcul de la taille de la grille
grid_size = instance.cube_size() * (11 if instance.enable_borders else 10)
#Dire au jeu que la grille fait grid_size
instance.set_grid_size(grid_size)

#Creation de la fenetre
window = pygame.display.set_mode((render_offset[0] * 4 + grid_size * 2, render_offset[1] * 2 + grid_size))
#On nomme la fenetre
pygame.display.set_caption("Bataille Navale")
#On y met une icone
pygame.display.set_icon(pygame.image.load("bato.jpg"))

#Variable de fermeture
should_close = False

#On charge l'arriere plan.
bg = pygame.image.load("mer.jpg").convert()
#On lui donne la taille de la fenetre
bg = pygame.transform.scale(bg, window.get_size())

#On calcule le nombre de case
size = (11 if instance.enable_borders else 10)
line_vert = pygame.surface.Surface((1, instance.cube_size() * size))
line_hori = pygame.surface.Surface((instance.cube_size() * size, 1))

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
