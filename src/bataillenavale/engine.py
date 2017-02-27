NULL = (0)
BOAT = (1)
DESTROYED = (2)
HIT_SUCCESS = (3)
HIT_MISS = (4)
DIRECTION_UP = (5)
DIRECTION_DOWN = (6)
DIRECTION_LEFT = (7)
DIRECTION_RIGHT = (8)
BOAT_CARRIER = (9) #Porte-Avion (5 cases)
BOAT_BATTLESHIP = (10) #Croiseur (4 cases)
BOAT_CRUISER = (11) #Contre-Torpilleur (3 cases)
BOAT_SUBMARINE = (12) #Sous-Marin (3 cases)
BOAT_DESTROYER = (13) #Torpilleur (2 cases)

class Player():
    
    def __init__(self): 
        self.grid = [[NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL]]
        self.opponent_grid = [[NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL],
                [NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL]]
        
    def place_boat(self, position, boat_type, direction):
        if not self.can_place_boat_at(position, boat_type, direction):
            return
        size = 0
        x_offset = 0
        y_offset = 0
        if direction == DIRECTION_UP:
            y_offset = 1
        elif direction == DIRECTION_DOWN:
            y_offset = -1
        elif direction == DIRECTION_LEFT:
            x_offset = -1
        elif direction == DIRECTION_RIGHT:
            x_offset = 1
        
        if boat_type == BOAT_CARRIER:
            size = 5
        elif boat_type == BOAT_BATTLESHIP:
            size = 4
        elif boat_type == BOAT_CRUISER or boat_type == BOAT_SUBMARINE:
            size = 3
        elif boat_type == BOAT_DESTROYER:
            size = 2
        for i in range(0, size):
            target = (position[0] + (x_offset * i), position[1] + (y_offset * i))
            self.grid[target[0]][target[1]] = BOAT
    
    def can_place_boat_at(self, position, boat_type, direction):
        size = 0
        if boat_type == BOAT_CARRIER:
            size = 5
        elif boat_type == BOAT_BATTLESHIP:
            size = 4
        elif boat_type == BOAT_CRUISER or boat_type == BOAT_SUBMARINE:
            size = 3
        elif boat_type == BOAT_DESTROYER:
            size = 2
        x_offset = 0
        y_offset = 0
        if direction == DIRECTION_UP:
            y_offset = 1
        elif direction == DIRECTION_DOWN:
            y_offset = -1
        elif direction == DIRECTION_LEFT:
            x_offset = -1
        elif direction == DIRECTION_RIGHT:
            x_offset = 1
        for i in range(0, size):
            target = (position[0] + (x_offset * i), position[1] + (y_offset * i))
            if not self.can_place_at(target):
                return False
        return True
    
    
    def can_place_at(self, position):
        if len(position) != 2:
            return False
        if position[0] < 0 or position[0] > 9:
            return False
        if position[1] < 0 or position[1] > 9:
            return False
        return self.grid[position[0]][position[1]] == NULL

    
    def attack(self, other, position = (0, 0)):
        if len(position) != 2:
            return
        if position[0] < 0 or position[0] > 9:
            return
        if position[1] < 0 or position[1] > 9:
            return
        self.opponent_grid[position[0]][position[1]] = other.handle_attack(position)
    
    def handle_attack(self, position):
        if len(position) != 2:
            return
        if position[0] < 0 or position[0] > 9:
            return
        if position[1] < 0 or position[1] > 9:
            return
        if (self.grid[position[0]][position[1]] == BOAT):
            self.grid[position[0]][position[1]] = DESTROYED
            return HIT_SUCCESS
        else:
            return HIT_MISS
