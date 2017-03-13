import pygame
from pygame.constants import *
from bataillenavale import game
from bataillenavale import engine
from bataillenavale.engine import DIRECTION_UP, BOAT_CARRIER
from bataillenavale.drawer import Drawer

def run_game():
    render_offset = (10, 10)
    
    #Ordre de taille de la grille.
    grid_size = 500
    #Initialisation de pygame
    print("Initialisation")
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
    
    prev_mouse_x = 0
    prev_mouse_y = 0
    
    drawer = Drawer(instance, render_offset)
    
    drawable_a = pygame.transform.scale(pygame.image.load("drawables/A.png"), (instance.cube_size(), instance.cube_size()))
    drawable_b = pygame.transform.scale(pygame.image.load("drawables/B.png"), (instance.cube_size(), instance.cube_size()))
    drawable_c = pygame.transform.scale(pygame.image.load("drawables/C.png"), (instance.cube_size(), instance.cube_size()))
    drawable_d = pygame.transform.scale(pygame.image.load("drawables/D.png"), (instance.cube_size(), instance.cube_size()))
    drawable_e = pygame.transform.scale(pygame.image.load("drawables/E.png"), (instance.cube_size(), instance.cube_size()))
    drawable_f = pygame.transform.scale(pygame.image.load("drawables/F.png"), (instance.cube_size(), instance.cube_size()))
    drawable_g = pygame.transform.scale(pygame.image.load("drawables/G.png"), (instance.cube_size(), instance.cube_size()))
    drawable_h = pygame.transform.scale(pygame.image.load("drawables/H.png"), (instance.cube_size(), instance.cube_size()))
    drawable_i = pygame.transform.scale(pygame.image.load("drawables/I.png"), (instance.cube_size(), instance.cube_size()))
    drawable_j = pygame.transform.scale(pygame.image.load("drawables/J.png"), (instance.cube_size(), instance.cube_size()))
   
    while not should_close:
        window.blit(bg, (0, 0))
        
        window.blit(drawable_a, (render_offset[0], render_offset[1] + instance.cube_size() * 1))
        window.blit(drawable_b, (render_offset[0], render_offset[1] + instance.cube_size() * 2))
        window.blit(drawable_c, (render_offset[0], render_offset[1] + instance.cube_size() * 3))
        window.blit(drawable_d, (render_offset[0], render_offset[1] + instance.cube_size() * 4))
        window.blit(drawable_e, (render_offset[0], render_offset[1] + instance.cube_size() * 5))
        window.blit(drawable_f, (render_offset[0], render_offset[1] + instance.cube_size() * 6))
        window.blit(drawable_g, (render_offset[0], render_offset[1] + instance.cube_size() * 7))
        window.blit(drawable_h, (render_offset[0], render_offset[1] + instance.cube_size() * 8))
        window.blit(drawable_i, (render_offset[0], render_offset[1] + instance.cube_size() * 9))
        window.blit(drawable_j, (render_offset[0], render_offset[1] + instance.cube_size() * 10))
        
        drawer.drawBoatAtPosition(window, prev_mouse_x, prev_mouse_y, BOAT_CARRIER, instance.rotation)
        
        for i in range(0, grid_size + 1, instance.cube_size()):
            window.blit(line_vert, (render_offset[0] + i, render_offset[1]))
            window.blit(line_hori, (render_offset[0], render_offset[1] + i))
            
            window.blit(line_vert, (render_offset[0] * 3 + grid_size + i, render_offset[1]))
            window.blit(line_hori, (render_offset[0] * 3 + grid_size, render_offset[1] + i))
        for event in pygame.event.get():
            if event.type == QUIT:
                print("Closing")
                should_close = True
            if event.type == MOUSEMOTION:
                prev_mouse_x = event.pos[0]
                prev_mouse_y = event.pos[1]
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    print ("Missed")
                elif event.button == 0:
                    instance.cycle_rotation()
        if not should_close:
            pygame.display.flip()
        else:
            pygame.quit()