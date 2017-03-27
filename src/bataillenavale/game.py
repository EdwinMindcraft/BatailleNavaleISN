from bataillenavale import engine
from bataillenavale.engine import DIRECTION_DOWN, PLAYER_1, PLAYER_2, NULL,\
    DIRECTION_LEFT, DIRECTION_UP, DIRECTION_RIGHT, Rules, BOAT_CARRIER,\
    BOAT_BATTLESHIP, BOAT_CRUISER, BOAT_SUBMARINE, BOAT_DESTROYER
from math import floor

class Game():
    def __init__(self, grid_scale, boat_selector_pos, enable_borders = True, rules = Rules()):
        self.rotation = DIRECTION_RIGHT
        self.rules = rules
        self.boat_selector_pos = boat_selector_pos
        self.player_1 = engine.Player(rules)
        self.player_2 = engine.Player(rules)
        self.turn = engine.PLAYER_1
        self.selected_boat_type = BOAT_CARRIER
        self.grid_scale = grid_scale
        self.enable_borders = enable_borders
    
    def is_won(self):
        if self.player_1.has_boat_left() and not self.player_2.has_boat_left():
            return PLAYER_1
        elif not self.player_1.has_boat_left() and self.player_2.has_boat_left():
            return PLAYER_2
        else:
            return NULL
    
    def get_boat_size(self, boat_type):
        size = 0
        if boat_type == BOAT_CARRIER:
            size = 5
        elif boat_type == BOAT_BATTLESHIP:
            size = 4
        elif boat_type == BOAT_CRUISER or boat_type == BOAT_SUBMARINE:
            size = 3
        elif boat_type == BOAT_DESTROYER:
            size = 2
        return size
    
    def set_grid_size(self, size):
        self.grid_scale = size
    
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
        return int(floor(num / size) * (size + (1 if self.enable_borders else 0)))
    
    def cube_size(self):
        return int(self.grid_scale / (11 if self.enable_borders else 10))
    
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
        
    def handle_play(self, mouse_x, mouse_y):
        if (mouse_x > self.boat_selector_pos[0] and mouse_x < self.boat_selector_pos[0] + 1020 and mouse_y > self.boat_selector_pos[1] and mouse_y < self.boat_selector_pos[1] + 500):
            pos_x = mouse_x - self.boat_selector_pos[0]
            pos_y = mouse_y - self.boat_selector_pos[1]
            
            return
        x = self.snap(mouse_x)
        y = self.snap(mouse_y)
        if (x < 0 or x > 9):
            return
        if (y < 0 or y > 9):
            return
        player = self.player_1 if self.turn == PLAYER_1 else self.player_2
        other = self.player_2 if self.turn == PLAYER_1 else self.player_1
        if player.opponent_grid[x][y] != NULL:
            return
        player.attack(other, (x, y))
    
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
        