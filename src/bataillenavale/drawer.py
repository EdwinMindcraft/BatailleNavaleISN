import pygame
from pygame.surface import Surface

from bataillenavale import engine
import bataillenavale.colorizer
from bataillenavale.engine import DIRECTION_UP, DIRECTION_LEFT, BOAT_CARRIER, \
    DIRECTION_DOWN, BOAT_BATTLESHIP, BOAT_CRUISER, BOAT_SUBMARINE, \
    BOAT_DESTROYER


class Drawer():
    def __init__(self, instance, render_offset, boat_selector_pos):
        self.instance = instance
        self.render_offset = render_offset
        self.boat_selector_pos = boat_selector_pos
        
        self.carrier = pygame.image.load("carrier.png").convert_alpha()
        self.carrier = pygame.transform.scale(self.carrier, (5 * instance.cube_size(), instance.cube_size()))
        
        self.battleship = pygame.image.load("battleship.png").convert_alpha()
        self.battleship = pygame.transform.scale(self.battleship, (4 * instance.cube_size(), instance.cube_size()))
        
        self.cruiser = pygame.image.load("cruiser.png").convert_alpha()
        self.cruiser = pygame.transform.scale(self.cruiser, (3 * instance.cube_size(), instance.cube_size()))
        
        self.submarine = pygame.image.load("submarine.png").convert_alpha()
        self.submarine = pygame.transform.scale(self.submarine, (3 * instance.cube_size(), instance.cube_size()))
        
        self.destroyer = pygame.image.load("destroyer.png").convert_alpha()
        self.destroyer = pygame.transform.scale(self.destroyer, (2 * instance.cube_size(), instance.cube_size()))
        
        self.carrier_invalid = self.carrier.copy()
        self.battleship_invalid = self.battleship.copy()
        self.cruiser_invalid = self.cruiser.copy()
        self.submarine_invalid = self.submarine.copy()
        self.destroyer_invalid = self.destroyer.copy()
        
        self.carrier_selected = self.carrier.copy()
        self.battleship_selected = self.battleship.copy()
        self.cruiser_selected = self.cruiser.copy()
        self.submarine_selected = self.submarine.copy()
        self.destroyer_selected = self.destroyer.copy()
        
        self.selector = Surface((1010, 400), pygame.SRCALPHA, 32).convert_alpha()
                
        bataillenavale.colorizer.create_invalid(self.carrier_invalid)
        bataillenavale.colorizer.create_invalid(self.battleship_invalid)
        bataillenavale.colorizer.create_invalid(self.cruiser_invalid)
        bataillenavale.colorizer.create_invalid(self.submarine_invalid)
        bataillenavale.colorizer.create_invalid(self.destroyer_invalid)
        
        bataillenavale.colorizer.create_selected(self.carrier_selected)
        bataillenavale.colorizer.create_selected(self.battleship_selected)
        bataillenavale.colorizer.create_selected(self.cruiser_selected)
        bataillenavale.colorizer.create_selected(self.submarine_selected)
        bataillenavale.colorizer.create_selected(self.destroyer_selected)

    def drawBoatAtPosition(self, window, mouseX, mouseY, boat_type, direction):
        place_pos_x = self.instance.snap(mouseX - self.render_offset[0]) * self.instance.cube_size() + self.render_offset[0] + self.instance.cube_size()
        place_pos_y = self.instance.snap(mouseY - self.render_offset[1]) * self.instance.cube_size() + self.render_offset[1] + self.instance.cube_size()
    
        canPlace = self.instance.can_place_boat(boat_type, place_pos_x, place_pos_y)
        self.draw_int(window, place_pos_x, place_pos_y, boat_type, direction, canPlace)
    
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

        self.selector.blit(carrier_text, (10, 10))
        self.selector.blit(battleship_text, (10, 65))
        self.selector.blit(cruiser_text, (10, 130))
        self.selector.blit(submarine_text, (510, 10))
        self.selector.blit(destroyer_text, (510, 65))
        window.blit(self.selector, self.boat_selector_pos)
        
    def drawBoard(self, window, instance):
        for pos in instance.get_current_player().carrier_pos:
            self.draw_int(window, self.render_offset[0] + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_CARRIER, pos[1], True)
        for pos in instance.get_current_player().battleship_pos:
            self.draw_int(window, self.render_offset[0] + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_BATTLESHIP, pos[1], True)
        for pos in instance.get_current_player().cruiser_pos:
            self.draw_int(window, self.render_offset[0] + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_CRUISER, pos[1], True)
        for pos in instance.get_current_player().submarine_pos:
            self.draw_int(window, self.render_offset[0] + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_SUBMARINE, pos[1], True)
        for pos in instance.get_current_player().destroyer_pos:
            self.draw_int(window, self.render_offset[0] + instance.cube_size() + pos[0][0] * instance.cube_size(), self.render_offset[1] + instance.cube_size() + pos[0][1] * instance.cube_size(), BOAT_DESTROYER, pos[1], True)
    
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

