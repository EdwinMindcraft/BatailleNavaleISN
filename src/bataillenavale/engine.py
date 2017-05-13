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
PLAYER_1 = (14)
PLAYER_2 = (15)

class Rules():
    def __init__(self):
        self.carrier_count = 1
        self.battleship_count = 1
        self.cruiser_count = 1
        self.submarine_count = 1
        self.destroyer_count = 1
    
    def set_boat_limit(self, boat_type, count):
        if (boat_type == BOAT_CARRIER):
            self.carrier_count = count
        elif (boat_type == BOAT_BATTLESHIP):
            self.battleship_count = count
        elif (boat_type == BOAT_CRUISER):
            self.cruiser_count = count
        elif (boat_type == BOAT_SUBMARINE):
            self.submarine_count = count
        elif (boat_type == BOAT_DESTROYER):
            self.destroyer_count = count
    
    def get_boat_limit(self, boat_type):
        if (boat_type == BOAT_CARRIER):
            return self.carrier_count
        elif (boat_type == BOAT_BATTLESHIP):
            return self.battleship_count
        elif (boat_type == BOAT_CRUISER):
            return self.cruiser_count
        elif (boat_type == BOAT_SUBMARINE):
            return self.submarine_count
        elif (boat_type == BOAT_DESTROYER):
            return self.destroyer_count
        else:
            return 0

class Player():
    
    def __init__(self, rules = Rules()):
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
        self.rules = rules
        self.carrier_placed = 0
        self.battleship_placed = 0
        self.cruiser_placed = 0
        self.submarine_placed = 0
        self.destroyer_placed = 0
        self.carrier_pos = []
        self.battleship_pos = []
        self.cruiser_pos = []
        self.submarine_pos = []
        self.destroyer_pos = []
        
    def place_boat(self, position, boat_type, direction):
        if not self.can_place_boat_at(position, boat_type, direction):
            return
        size = 0
        x_offset = 0
        y_offset = 0
        if direction == DIRECTION_UP:
            y_offset = -1
        elif direction == DIRECTION_DOWN:
            y_offset = 1
        elif direction == DIRECTION_LEFT:
            x_offset = -1
        elif direction == DIRECTION_RIGHT:
            x_offset = 1
        
        if boat_type == BOAT_CARRIER:
            size = 5
            self.carrier_pos.append((position, direction))
            self.carrier_placed += 1
        elif boat_type == BOAT_BATTLESHIP:
            size = 4
            self.battleship_pos.append((position, direction))
            self.battleship_placed += 1
        elif boat_type == BOAT_CRUISER:
            size = 3
            self.cruiser_pos.append((position, direction))
            self.cruiser_placed += 1
        elif boat_type == BOAT_SUBMARINE:
            size = 3
            self.submarine_pos.append((position, direction))
            self.submarine_placed += 1
        elif boat_type == BOAT_DESTROYER:
            size = 2
            self.destroyer_pos.append((position, direction))
            self.destroyer_placed += 1
        for i in range(0, size):
            target = (position[0] + (x_offset * i), position[1] + (y_offset * i))
            self.grid[target[0]][target[1]] = BOAT
    
    def get_boat_count(self, boat_type):
        if (boat_type == BOAT_CARRIER):
            return self.carrier_placed
        elif (boat_type == BOAT_BATTLESHIP):
            return self.battleship_placed
        elif (boat_type == BOAT_CRUISER):
            return self.cruiser_placed
        elif (boat_type == BOAT_SUBMARINE):
            return self.submarine_placed
        elif (boat_type == BOAT_DESTROYER):
            return self.destroyer_placed
        else:
            return 0
        
    def can_place_boat_at(self, position, boat_type, direction):
        if (self.rules.get_boat_limit(boat_type) <= self.get_boat_count(boat_type)):
            return False
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
            y_offset = -1
        elif direction == DIRECTION_DOWN:
            y_offset = 1
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
    
    def should_switch(self):
        carrier_left = self.rules.get_boat_limit(BOAT_CARRIER) - self.carrier_placed
        battleship_left = self.rules.get_boat_limit(BOAT_BATTLESHIP) - self.battleship_placed
        cruiser_left = self.rules.get_boat_limit(BOAT_CRUISER) - self.cruiser_placed
        destroyer_left = self.rules.get_boat_limit(BOAT_DESTROYER) - self.destroyer_placed
        submarine_left = self.rules.get_boat_limit(BOAT_SUBMARINE) - self.submarine_placed
        return carrier_left <= 0 and battleship_left <= 0 and cruiser_left <= 0 and destroyer_left <= 0 and submarine_left <= 0
    
    def has_boat_left(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] == BOAT:
                    return True
        return False
