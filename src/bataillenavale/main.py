import pygame
import socket
from pygame.constants import *

from bataillenavale import engine
from bataillenavale import game
from bataillenavale.drawer import Drawer
from bataillenavale.engine import PLAYER_1, NULL


def run_game(local=True, host=True, host_name=socket.gethostname()):
    
    render_offset = (10, 60)
    place_grid_position = (10, 560)
    
    #Ordre de taille de la grille.
    grid_size = 500
    #Initialisation de pygame
    pygame.init()
    
    #Regles
    rules = engine.Rules()
        
    #Creation de l'instance du jeu
    instance = game.Game(grid_size, place_grid_position, rules=rules)
    if not local:
        if host:
            instance.initHost()
        else:
            instance.initClient(host_name)

    
    #Calcul de la taille de la grille
    grid_size = instance.cube_size() * (11 if instance.enable_borders else 10)
    #Dire au jeu que la grille fait grid_size
    instance.set_grid_size(grid_size)
    
    #Creation de la fenetre
    window = pygame.display.set_mode((render_offset[0] * 4 + grid_size * 2, render_offset[1] * 2 + grid_size + 400))
    #On nomme la fenetre
    pygame.display.set_caption("Bataille Navale")
    #On y met une icone
    pygame.display.set_icon(pygame.image.load("drawables/icon.png"))
    
    #Variable de fermeture
    should_close = False
    
    #On charge l'arriere plan.
    bg = pygame.image.load("drawables/background.png").convert()
    #On lui donne la taille de la fenetre
    bg = pygame.transform.scale(bg, window.get_size())
    
    #On calcule le nombre de case
    size = (11 if instance.enable_borders else 10)
    #On creer les barres qui vont separer les cases
    line_vert = pygame.surface.Surface((1, instance.cube_size() * size + 1))
    line_hori = pygame.surface.Surface((instance.cube_size() * size + 1, 1))
    
    #On defini les position de souris. Elle permettent de faire des equivalent de boutons
    prev_mouse_x = 0
    prev_mouse_y = 0
    
    #On creer le drawer, celui qui contient la majorite des choses a dessiner
    drawer = Drawer(instance, render_offset, place_grid_position, window)
    #On charge les lettres et les chiffres.
    drawables = [0]*22
    
    drawables[0] = pygame.transform.scale(pygame.image.load("drawables/A.png"), (instance.cube_size(), instance.cube_size()))
    drawables[1] = pygame.transform.scale(pygame.image.load("drawables/B.png"), (instance.cube_size(), instance.cube_size()))
    drawables[2] = pygame.transform.scale(pygame.image.load("drawables/C.png"), (instance.cube_size(), instance.cube_size()))
    drawables[3] = pygame.transform.scale(pygame.image.load("drawables/D.png"), (instance.cube_size(), instance.cube_size()))
    drawables[4] = pygame.transform.scale(pygame.image.load("drawables/E.png"), (instance.cube_size(), instance.cube_size()))
    drawables[5] = pygame.transform.scale(pygame.image.load("drawables/F.png"), (instance.cube_size(), instance.cube_size()))
    drawables[6] = pygame.transform.scale(pygame.image.load("drawables/G.png"), (instance.cube_size(), instance.cube_size()))
    drawables[7] = pygame.transform.scale(pygame.image.load("drawables/H.png"), (instance.cube_size(), instance.cube_size()))
    drawables[8] = pygame.transform.scale(pygame.image.load("drawables/I.png"), (instance.cube_size(), instance.cube_size()))
    drawables[9] = pygame.transform.scale(pygame.image.load("drawables/J.png"), (instance.cube_size(), instance.cube_size()))
    
    drawables[10] = pygame.transform.scale(pygame.image.load("drawables/1.png"), (instance.cube_size(), instance.cube_size()))
    drawables[11] = pygame.transform.scale(pygame.image.load("drawables/2.png"), (instance.cube_size(), instance.cube_size()))
    drawables[12] = pygame.transform.scale(pygame.image.load("drawables/3.png"), (instance.cube_size(), instance.cube_size()))
    drawables[13] = pygame.transform.scale(pygame.image.load("drawables/4.png"), (instance.cube_size(), instance.cube_size()))
    drawables[14] = pygame.transform.scale(pygame.image.load("drawables/5.png"), (instance.cube_size(), instance.cube_size()))
    drawables[15] = pygame.transform.scale(pygame.image.load("drawables/6.png"), (instance.cube_size(), instance.cube_size()))
    drawables[16] = pygame.transform.scale(pygame.image.load("drawables/7.png"), (instance.cube_size(), instance.cube_size()))
    drawables[17] = pygame.transform.scale(pygame.image.load("drawables/8.png"), (instance.cube_size(), instance.cube_size()))
    drawables[18] = pygame.transform.scale(pygame.image.load("drawables/9.png"), (instance.cube_size(), instance.cube_size()))
    drawables[19] = pygame.transform.scale(pygame.image.load("drawables/10.png"), (instance.cube_size(), instance.cube_size()))
    
    drawables[20] = pygame.transform.scale(pygame.image.load("drawables/tour_j1.png"), (400, 60))
    drawables[21] = pygame.transform.scale(pygame.image.load("drawables/tour_j2.png"), (400, 60))
    
    #Ici on met a jour la fenetre.
    while not should_close:
        window.blit(bg, (0, 0)) #On dessine l'arriere plan
        if instance.victor == NULL:
            if (instance.turn == PLAYER_1):
                window.blit(drawables[20], ((window.get_size()[0] - drawables[20].get_width()) / 2, 10))
            else:
                window.blit(drawables[21], ((window.get_size()[0] - drawables[21].get_width()) / 2, 10))            
            
            #On ecrit les lettres et les chiffres sur les 2 grilles
            for i in range(0, 10):
                window.blit(drawables[i], (render_offset[0], render_offset[1] + instance.cube_size() * (i + 1)))
                window.blit(drawables[i], (render_offset[0] * 3 + grid_size, render_offset[1] + instance.cube_size() * (i + 1)))
                
                window.blit(drawables[10 + i], (render_offset[0] + instance.cube_size() * (i + 1), render_offset[1]))
                window.blit(drawables[10 + i], (render_offset[0] * 3 + grid_size + instance.cube_size() * (i + 1), render_offset[1]))
    
            #On dessine le bateau selectionne si la souris est sur la premiere grille et que l'on est dans le mode initialisation
            if (instance.is_placing and prev_mouse_x - render_offset[0] > 0 and prev_mouse_x - render_offset[0] < grid_size and prev_mouse_y -render_offset[1] > 0 and prev_mouse_y - render_offset[1] < grid_size):
                drawer.drawBoatAtPosition(prev_mouse_x, prev_mouse_y, instance.selected_boat_type, instance.rotation)
            
            #On dessine les bateaus sur la grille.
            drawer.drawBoard()
            #On dessine la grille de selection des bateaus
            drawer.drawBoatSelector()
            #On dessine les lignes qui limite les cases des grilles
            for i in range(0, grid_size + 1, instance.cube_size()):
                window.blit(line_vert, (render_offset[0] + i, render_offset[1]))
                window.blit(line_hori, (render_offset[0], render_offset[1] + i))
                
                window.blit(line_vert, (render_offset[0] * 3 + grid_size + i, render_offset[1]))
                window.blit(line_hori, (render_offset[0] * 3 + grid_size, render_offset[1] + i))
        else:
            drawer.drawVictoryScreen()
        
        #On regarge les evenements que la fenetre recois (Clics, Mouvements de souris...)
        for event in pygame.event.get():
            if event.type == QUIT: #Si l'evenement est fermer la fenetre (la croix)...
                if not instance.client is None:
                    instance.client.close()
                if not instance.server is None:
                    instance.server.close()
                should_close = True #...on arrete la boucle, donc on termine le programme
            if event.type == MOUSEMOTION: #Si l'evenement est un mouvement de souris...
                #...on stocke la nouvelle position de la souris
                prev_mouse_x = event.pos[0]
                prev_mouse_y = event.pos[1]
            if event.type == MOUSEBUTTONUP: #Lorsque l'on lache le clic...
                if event.button == 1: #Clic gauche
                    instance.handle_play(prev_mouse_x - render_offset[0], prev_mouse_y - render_offset[1]) #On joue.
                elif event.button == 3 and instance.is_placing: #Clic droit
                    instance.cycle_rotation() #On change la rotation du placement du bateau
        if not should_close: #Si on ne doit pas fermer...
            pygame.display.flip() #On actualise la fenetre.
        else: # Sinon...
            pygame.quit() #On detruis l'objet pygame, pour eviter de saturer la memoire.
            if not instance.local:
                if not instance.server is None:
                    instance.server.close()
                if not instance.client is None:
                    instance.client.close()
                if not instance.thread is None:
                    instance.thread.kill()