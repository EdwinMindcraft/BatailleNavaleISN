import pygame
from pygame.surface import Surface

from bataillenavale import engine
import bataillenavale.colorizer
import time
from bataillenavale.engine import DIRECTION_UP, DIRECTION_LEFT, BOAT_CARRIER, \
    DIRECTION_DOWN, BOAT_BATTLESHIP, BOAT_CRUISER, BOAT_SUBMARINE, \
    BOAT_DESTROYER, HIT_SUCCESS, HIT_MISS, DESTROYED, PLAYER_1, HIT_DESTROYED


class Drawer():
    """
    instance: Instance de Game, correspont au données du jeu.
    render_offset: Decalage des grilles par rapport au haut de la fenetre (format: x, y)
    boat_selector_pos: Decalage du panneau de selection des bateaux par rapport au haut de la fenetre (format: x, y)
    """
    def __init__(self, instance, render_offset, boat_selector_pos):
        #Declaration de variable
        self.instance = instance
        self.render_offset = render_offset
        self.boat_selector_pos = boat_selector_pos
        self.lastTime = -1;
        self.current_player = PLAYER_1
        
        #Creation des image
        #Porte-Avion
        self.carrier = pygame.image.load("carrier.png").convert_alpha()
        self.carrier = pygame.transform.scale(self.carrier, (5 * instance.cube_size(), instance.cube_size()))
        #Croiseur
        self.battleship = pygame.image.load("battleship.png").convert_alpha()
        self.battleship = pygame.transform.scale(self.battleship, (4 * instance.cube_size(), instance.cube_size()))
        #Contre-Torpilleur
        self.cruiser = pygame.image.load("cruiser.png").convert_alpha()
        self.cruiser = pygame.transform.scale(self.cruiser, (3 * instance.cube_size(), instance.cube_size()))
        #Sous-Marin
        self.submarine = pygame.image.load("submarine.png").convert_alpha()
        self.submarine = pygame.transform.scale(self.submarine, (3 * instance.cube_size(), instance.cube_size()))
        #Torpilleur
        self.destroyer = pygame.image.load("destroyer.png").convert_alpha()
        self.destroyer = pygame.transform.scale(self.destroyer, (2 * instance.cube_size(), instance.cube_size()))
        
        #Effet de touche.
        self.hit = pygame.image.load("hit.png").convert_alpha()
        self.hit = pygame.transform.scale(self.hit, (instance.cube_size(), instance.cube_size()))
        
        #Effet lorque l'on rate
        self.miss = pygame.image.load("miss.png").convert_alpha()
        self.miss = pygame.transform.scale(self.miss, (instance.cube_size(), instance.cube_size()))
        
        #Effet lorque qu'un bateau est detruit (Ennemi) ou quand un bateau subit des tir (Joueur)
        self.destroyed = pygame.image.load("destroyed.png").convert_alpha()
        self.destroyed = pygame.transform.scale(self.destroyed, (instance.cube_size(), instance.cube_size()))
        
        #Versions rouge (invalides) des bateaux
        #Copies des images.
        self.carrier_invalid = self.carrier.copy()
        self.battleship_invalid = self.battleship.copy()
        self.cruiser_invalid = self.cruiser.copy()
        self.submarine_invalid = self.submarine.copy()
        self.destroyer_invalid = self.destroyer.copy()
        
        #Filtres rouges.
        bataillenavale.colorizer.create_invalid(self.carrier_invalid)
        bataillenavale.colorizer.create_invalid(self.battleship_invalid)
        bataillenavale.colorizer.create_invalid(self.cruiser_invalid)
        bataillenavale.colorizer.create_invalid(self.submarine_invalid)
        bataillenavale.colorizer.create_invalid(self.destroyer_invalid)
        
        #Versions verte (selectionnes) des bateaux
        #Copies des images.
        self.carrier_selected = self.carrier.copy()
        self.battleship_selected = self.battleship.copy()
        self.cruiser_selected = self.cruiser.copy()
        self.submarine_selected = self.submarine.copy()
        self.destroyer_selected = self.destroyer.copy()
        
        #Filtres verts.
        bataillenavale.colorizer.create_selected(self.carrier_selected)
        bataillenavale.colorizer.create_selected(self.battleship_selected)
        bataillenavale.colorizer.create_selected(self.cruiser_selected)
        bataillenavale.colorizer.create_selected(self.submarine_selected)
        bataillenavale.colorizer.create_selected(self.destroyer_selected)
        
        #Surface pour le selecteur
        self.selector = Surface((1020, 400), pygame.SRCALPHA, 32).convert_alpha()
        
    """
    Dessine un bateau a la position choisie
    window: La fenetre du selecteur.
    mouseX: Position en X de la souris
    mouseY: Position en Y de la souris
    boat_type: Type de bateau
    direction: Orientation du bateau
    """
    def drawBoatAtPosition(self, window, mouseX, mouseY, boat_type, direction):
        #Force les postions pour rentrer dans la grille.
        place_pos_x = self.instance.snap(mouseX - self.render_offset[0]) * self.instance.cube_size() + self.render_offset[0] + self.instance.cube_size()
        place_pos_y = self.instance.snap(mouseY - self.render_offset[1]) * self.instance.cube_size() + self.render_offset[1] + self.instance.cube_size()
        
        #Verifie si on peu placer le bateau
        canPlace = self.instance.can_place_boat(boat_type, place_pos_x, place_pos_y - self.instance.cube_size())
        #On dessine le bateau
        self.draw_int(window, place_pos_x, place_pos_y, boat_type, direction, canPlace)
    
    """
    Fonction interne pour dessiner le bateau, evite les positions forcés de drawBoatAtPosition
    """
    def draw_int(self, window, place_pos_x, place_pos_y, boat_type, direction, canPlace):
        texture = self.getBoatTexture(boat_type, canPlace)
        if (direction == DIRECTION_UP):
            texture = pygame.transform.rotate(texture, 90)
            place_pos_y -= (self.instance.get_boat_size(boat_type) - 1) * self.instance.cube_size()
        elif (direction == DIRECTION_LEFT):
            texture = pygame.transform.rotate(texture, 180)
            place_pos_x -= (self.instance.get_boat_size(boat_type) - 1) * self.instance.cube_size()
        elif (direction == DIRECTION_DOWN):
            texture = pygame.transform.rotate(texture, 270)
        
        window.blit(texture, (place_pos_x, place_pos_y))
    
    """
    Dessine le selecteur de bateau.
    
    Le format est le meme:
    Pour chaque bateau, on choisie la texture.
    En priotite le bateaux invalide, puis le selectionne et enfin celui sans rien.
    
    Ensuite on dessine les bordures, puis les bateaux.
    """
    def drawBoatSelector(self, window, instance):
        carrier_text = self.carrier
        if (instance.get_current_player().get_boat_count(BOAT_CARRIER) >= instance.rules.get_boat_limit(BOAT_CARRIER)):
            carrier_text = self.carrier_invalid
        elif (instance.selected_boat_type == BOAT_CARRIER):
            carrier_text = self.carrier_selected
        
        battleship_text = self.battleship
        if (instance.get_current_player().get_boat_count(BOAT_BATTLESHIP) >= instance.rules.get_boat_limit(BOAT_BATTLESHIP)):
            battleship_text = self.battleship_invalid
        elif (instance.selected_boat_type == BOAT_BATTLESHIP):
            battleship_text = self.battleship_selected

        cruiser_text = self.cruiser
        if (instance.get_current_player().get_boat_count(BOAT_CRUISER) >= instance.rules.get_boat_limit(BOAT_CRUISER)):
            cruiser_text = self.cruiser_invalid
        elif (instance.selected_boat_type == BOAT_CRUISER):
            cruiser_text = self.cruiser_selected

        submarine_text = self.submarine
        if (instance.get_current_player().get_boat_count(BOAT_SUBMARINE) >= instance.rules.get_boat_limit(BOAT_SUBMARINE)):
            submarine_text = self.submarine_invalid
        elif (instance.selected_boat_type == BOAT_SUBMARINE):
            submarine_text = self.submarine_selected

        destroyer_text = self.destroyer
        if (instance.get_current_player().get_boat_count(BOAT_DESTROYER) >= instance.rules.get_boat_limit(BOAT_DESTROYER)):
            destroyer_text = self.destroyer_invalid
        elif (instance.selected_boat_type == BOAT_DESTROYER):
            destroyer_text = self.destroyer_selected
            
            
        self.selector.blit(Surface((1, 185)), (0, 0))
        self.selector.blit(Surface((instance.grid_scale * 2 + self.render_offset[0] * 2, 1)), (0, 0))
        self.selector.blit(Surface((1, 185)), (instance.grid_scale * 2 + self.render_offset[0] * 2, 0))
        self.selector.blit(Surface((instance.grid_scale * 2 + self.render_offset[0] * 2 + 1, 1)), (0, 185))
        
        self.selector.blit(carrier_text, (10, 10))
        self.selector.blit(battleship_text, (10, 65))
        self.selector.blit(cruiser_text, (10, 130))
        self.selector.blit(submarine_text, (510, 10))
        self.selector.blit(destroyer_text, (510, 65))
        #On "colle" le selecteur sur la fenetre.
        window.blit(self.selector, self.boat_selector_pos)
    
    """
    Dessine le terrain de jeu (bateau + effets)
    """
    def drawBoard(self, window, instance):
        #On recupere le joueur.
        if (self.current_player != instance.turn):
            if (self.lastTime == -1):
                self.lastTime = time.time()
                print("Time : " + str(self.lastTime))
                instance.locked = True
            if (self.lastTime + 5 < time.time()):
                self.lastTime = -1
                print ("Updating screen : " + str(time.time()))
                self.current_player = instance.turn
                instance.locked = False
        player = instance.player_1 if self.current_player == PLAYER_1 else instance.player_2
        #Si on est en train de placer les bateaux, on affiche les bateaux sur la grille de gauche.
        #Sinon on les affiche sur la grille de droite.
        offset_x = 0 if instance.is_placing else instance.grid_scale + self.render_offset[0] * 2
        #On dessine les bateaux.
        for pos in player.carrier_pos:
            self.draw_int(window, self.render_offset[0] + offset_x + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_CARRIER, pos[1], True)
        for pos in player.battleship_pos:
            self.draw_int(window, self.render_offset[0] + offset_x + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_BATTLESHIP, pos[1], True)
        for pos in player.cruiser_pos:
            self.draw_int(window, self.render_offset[0] + offset_x + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_CRUISER, pos[1], True)
        for pos in player.submarine_pos:
            self.draw_int(window, self.render_offset[0] + offset_x + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_SUBMARINE, pos[1], True)
        for pos in player.destroyer_pos:
            self.draw_int(window, self.render_offset[0] + offset_x + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_DESTROYER, pos[1], True)
        
        #On passe a travers la grille adverse.
        for x in range(0, len(player.opponent_grid)):
            for y in range(0, len(player.opponent_grid[x])):
                #Pour chaque coup reussi, on dessinne une explosion
                if (player.opponent_grid[x][y] == HIT_SUCCESS):
                    window.blit(self.hit, (self.render_offset[0] + (instance.cube_size() * (x+1)), self.render_offset[1] + (instance.cube_size() * (y+1))))
                #Les tirs rates sont representes par une croix
                elif (player.opponent_grid[x][y] == HIT_MISS):
                    window.blit(self.miss, (self.render_offset[0] + (instance.cube_size() * (x+1)), self.render_offset[1] + (instance.cube_size() * (y+1))))
                #Et les bateaux que l'on a detruit s'affiche en flame.
                elif (player.opponent_grid[x][y] == HIT_DESTROYED):
                    window.blit(self.destroyed, (self.render_offset[0] + (instance.cube_size() * (x+1)), self.render_offset[1] + (instance.cube_size() * (y+1))))
        #On passe a travers notre grille.
        for x in range(0, len(player.grid)):
            for y in range(0, len(player.grid[x])):
                #Si la case a pris un coup, on met des flammes.
                if (player.grid[x][y] == DESTROYED):
                    window.blit(self.destroyed, (self.render_offset[0] * 3 + instance.grid_scale + (instance.cube_size() * (x+1)), self.render_offset[1] + (instance.cube_size() * (y+1))))
    """
    Cette methode permet de ne pas perdre 300 ans a reecrire 20000 fois les memes lignes de code.
    Elle permet d'obtenir facilement la texture d'un bateau.
    """
    def getBoatTexture (self, boat_type, valid):
        if (boat_type == BOAT_CARRIER):
            return self.carrier if valid else self.carrier_invalid
        elif (boat_type == BOAT_BATTLESHIP):
            return self.battleship if valid else self.battleship_invalid
        elif (boat_type == BOAT_CRUISER):
            return self.cruiser if valid else self.cruiser_invalid
        elif (boat_type == BOAT_SUBMARINE):
            return self.submarine if valid else self.submarine_invalid
        elif (boat_type == BOAT_DESTROYER):
            return self.destroyer if valid else self.destroyer_invalid

