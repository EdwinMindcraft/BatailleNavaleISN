import pygame
from bataillenavale import engine
from bataillenavale.engine import DIRECTION_UP, DIRECTION_LEFT, BOAT_CARRIER,\
    DIRECTION_DOWN, BOAT_BATTLESHIP, BOAT_CRUISER, BOAT_SUBMARINE,\
    BOAT_DESTROYER
import bataillenavale.colorizer
from pygame.surface import Surface


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
        
        self.submarime = pygame.image.load("submarine.png").convert_alpha()
        self.submarime = pygame.transform.scale(self.submarime, (3 * instance.cube_size(), instance.cube_size()))
        
        self.destroyer = pygame.image.load("destroyer.png").convert_alpha()
        self.destroyer = pygame.transform.scale(self.destroyer, (2 * instance.cube_size(), instance.cube_size()))
        
        self.carrier_invalid = self.carrier.copy()
        self.battleship_invalid = self.battleship.copy()
        self.cruiser_invalid = self.cruiser.copy()
        self.submarime_invalid = self.submarime.copy()
        self.destroyer_invalid = self.destroyer.copy()
        
        self.selector = Surface((1010, 500))
                
        bataillenavale.colorizer.create_invalid(self.carrier_invalid)
        bataillenavale.colorizer.create_invalid(self.battleship_invalid)
        bataillenavale.colorizer.create_invalid(self.cruiser_invalid)
        bataillenavale.colorizer.create_invalid(self.submarime_invalid)
        bataillenavale.colorizer.create_invalid(self.destroyer_invalid)
        
        

    def drawBoatAtPosition(self, window, mouseX, mouseY, boat_type, direction):
        place_pos_x = self.instance.snap(mouseX - self.render_offset[0]) * self.instance.cube_size() + self.render_offset[0] + self.instance.cube_size()
        place_pos_y = self.instance.snap(mouseY - self.render_offset[1]) * self.instance.cube_size() + self.render_offset[1] + self.instance.cube_size()
    
        canPlace = self.instance.can_place_boat(boat_type, place_pos_x, place_pos_y)
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
    
    def drawBoatSelector(self, window):
        self.selector.blit(self.carrier, (10, 10))
        window.blit(self.selector, self.boat_selector_pos)
    
    def getBoatTexture (self, boat_type, valid):
        if (boat_type == BOAT_CARRIER):
            return self.carrier if valid else self.carrier_invalid
        elif (boat_type == BOAT_BATTLESHIP):
            return self.battleship if valid else self.battleship_invalid
        elif (boat_type == BOAT_CRUISER):
            return self.cruiser if valid else self.cruiser_invalid
        elif (boat_type == BOAT_SUBMARINE):
            return self.submarime if valid else self.submarime_invalid
        elif (boat_type == BOAT_DESTROYER):
            return self.destroyer if valid else self.destroyer_invalid

