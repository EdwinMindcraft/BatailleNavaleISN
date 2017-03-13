import pygame
from bataillenavale import engine
from bataillenavale.engine import DIRECTION_UP, DIRECTION_LEFT, BOAT_CARRIER,\
    DIRECTION_DOWN


class Drawer():
    def __init__(self, instance, render_offset):
        self.instance = instance
        self.render_offset = render_offset
        self.carrier = pygame.image.load("carrier.png").convert_alpha()
        self.carrier = pygame.transform.scale(self.carrier, (5 * instance.cube_size(), instance.cube_size()))
        
        self.carrier_invalid = pygame.image.load("carrier.png").convert_alpha()
        self.carrier_invalid = pygame.transform.scale(self.carrier_invalid, (5 * instance.cube_size(), instance.cube_size()))
        self.carrier_invalid.set_masks((0, 127, 127, 0))
        

    def drawBoatAtPosition(self, window, mouseX, mouseY, boat_type, direction):
        place_pos_x = self.instance.snap(mouseX - self.render_offset[0]) * self.instance.cube_size() + self.render_offset[0]
        place_pos_y = self.instance.snap(mouseY - self.render_offset[1]) * self.instance.cube_size() + self.render_offset[1]
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
    
    def getBoatTexture (self, boat_type, valid):
        if (boat_type == BOAT_CARRIER):
            return self.carrier if valid else self.carrier_invalid