from bataillenavale import engine
from bataillenavale.engine import DIRECTION_DOWN, PLAYER_1, PLAYER_2, NULL,\
    DIRECTION_LEFT, DIRECTION_UP, DIRECTION_RIGHT
from math import floor

class Game():
    def __init__(self, grid_scale, enable_borders = True):
        self.rotation = DIRECTION_DOWN
        self.player_1 = engine.Player()
        self.player_2 = engine.Player()
        self.turn = engine.PLAYER_1
        self.grid_scale = grid_scale
        self.enable_borders = enable_borders
    
    def is_won(self):
        if self.player_1.has_boat_left() and not self.player_2.has_boat_left():
            return PLAYER_1
        elif not self.player_1.has_boat_left() and self.player_2.has_boat_left():
            return PLAYER_2
        else:
            return NULL
    
    def cycle_rotation(self):
        if (self.rotation == DIRECTION_DOWN):
            self.rotation = DIRECTION_LEFT
        elif (self.rotation == DIRECTION_LEFT):
            self.rotation = DIRECTION_UP
        elif (self.rotation == DIRECTION_UP):
            self.rotation = DIRECTION_RIGHT
        else:
            self.rotation = DIRECTION_DOWN
    
    def snap(self, num):
        size = self.grid_scale / (11 if self.enable_borders else 10)
        return floor(num / size) - (1 if self.enable_borders else 0)
    
    def render_snap(self, num):
        size = self.grid_scale / (11 if self.enable_borders else 10)
        return floor(num / size) * size       
    
    def can_place_boat(self, boat_type, mouse_x, mouse_y):
        x = self.snap(mouse_x)
        y = self.snap(mouse_y)
        if (x < 0 or x > 9):
            return False
        if (y < 0 or y > 9):
            return False
        if (self.turn == PLAYER_1):
            return self.player_1.can_place_boat_at((x, y), boat_type, self.rotation)
        else:
            return self.player_2.can_place_boat_at((x, y), boat_type, self.rotation)
    
    def place_boat_at(self, boat_type, mouse_x, mouse_y):
        x = self.snap(mouse_x)
        y = self.snap(mouse_y)
        if (x < 0 or x > 9):
            return False
        if (y < 0 or y > 9):
            return False
        if not self.can_place_boat(boat_type, mouse_x, mouse_y):
            return False
        if (self.turn == PLAYER_1):
            self.player_1.place_boat((x, y), boat_type, self.rotation)
        else:
            self.player_2.place_boat((x, y), boat_type, self.rotation)
        return True
        