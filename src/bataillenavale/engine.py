"""
Variables Globales.
Elle permettent de rendre le code plus digeste.
On pourrais en theorie les remplaces par leurs nombres respectif mais ce serais illisible.
"""
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
HIT_DESTROYED = (16)

"""
Les regles.
Pas tres utiles, mais elle permettents une plus grande simplicite
"""
class Rules():
    def __init__(self):
        self.carrier_count = 1
        self.battleship_count = 1
        self.cruiser_count = 1
        self.submarine_count = 1
        self.destroyer_count = 1
    """
    Definit la limite de bateau d'un type.
    """
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
    """
    Recupere le nombre maximum de bateau d'un type.
    """
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
    """
    Place un bataux a la position ciblee.
    """
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
    """
    Recupere le nombre de bateaux d'un type places.
    """
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
    """
    Verifie que l'on peut bien placer un bateau la ou on veut
    """
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
    """
    Verifie que la case ciblee est vide.
    """
    def can_place_at(self, position):
        if len(position) != 2:
            return False
        if position[0] < 0 or position[0] > 9:
            return False
        if position[1] < 0 or position[1] > 9:
            return False
        return self.grid[position[0]][position[1]] == NULL
    """
    A L'ATTAQUE!
    Plus serieusement cette fonction permet d'attaquer une case.
    """
    def attack(self, other, position = (0, 0)):
        if len(position) != 2:
            return
        if position[0] < 0 or position[0] > 9:
            return
        if position[1] < 0 or position[1] > 9:
            return
        attack = other.handle_attack(position)
        print(attack)
        if attack[0] == HIT_DESTROYED:
            for loc in attack[1]:
                self.opponent_grid[loc[0]][loc[1]] = HIT_DESTROYED
        else:
            self.opponent_grid[position[0]][position[1]] = attack[0]
        for row in self.opponent_grid:
            print(row)
    
    """
    On gere l'attaque du cote de la personne qui se fait attaquer.
    """
    def handle_attack(self, position):
        if len(position) != 2:
            return
        if position[0] < 0 or position[0] > 9:
            return
        if position[1] < 0 or position[1] > 9:
            return
        if (self.grid[position[0]][position[1]] == BOAT):
            self.grid[position[0]][position[1]] = DESTROYED
            #Carrier
            for pos in self.carrier_pos:
                location = pos[0]
                direction = pos[1]
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
                destroyed = True;
                isContained = False
                locs = []
                for i in range(0, 5):
                    newLoc = (location[0] + (x_offset * i), location[1] + (y_offset * i))
                    if newLoc == position:
                        isContained = True
                    locs.append(newLoc)
                    if not self.grid[newLoc[0]][newLoc[1]] == DESTROYED:
                        destroyed = False;
                if destroyed and isContained:
                    return (HIT_DESTROYED, locs)
            #Battleship
            for pos in self.battleship_pos:
                location = pos[0]
                direction = pos[1]
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
                destroyed = True;
                isContained = False
                locs = []
                for i in range(0, 4):
                    newLoc = (location[0] + (x_offset * i), location[1] + (y_offset * i))
                    locs.append(newLoc)
                    if newLoc == position:
                        isContained = True
                    if not self.grid[newLoc[0]][newLoc[1]] == DESTROYED:
                        destroyed = False;
                if destroyed and isContained:
                    return (HIT_DESTROYED, locs)
            #Cruiser
            for pos in self.cruiser_pos:
                location = pos[0]
                direction = pos[1]
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
                destroyed = True;
                isContained = False
                locs = []
                for i in range(0, 3):
                    newLoc = (location[0] + (x_offset * i), location[1] + (y_offset * i))
                    locs.append(newLoc)
                    if newLoc == position:
                        isContained = True
                    if not self.grid[newLoc[0]][newLoc[1]] == DESTROYED:
                        destroyed = False;
                if destroyed and isContained:
                    return (HIT_DESTROYED, locs)
            #Submarine
            for pos in self.submarine_pos:
                location = pos[0]
                direction = pos[1]
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
                destroyed = True;
                isContained = False
                locs = []
                for i in range(0, 3):
                    newLoc = (location[0] + (x_offset * i), location[1] + (y_offset * i))
                    locs.append(newLoc)
                    if newLoc == position:
                        isContained = True
                    if not self.grid[newLoc[0]][newLoc[1]] == DESTROYED:
                        destroyed = False;
                if destroyed and isContained:
                    return (HIT_DESTROYED, locs)
            #Destroyer
            for pos in self.destroyer_pos:
                location = pos[0]
                direction = pos[1]
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
                destroyed = True;
                isContained = False
                locs = []
                for i in range(0, 2):
                    newLoc = (location[0] + (x_offset * i), location[1] + (y_offset * i))
                    locs.append(newLoc)
                    if newLoc == position:
                        isContained = True
                    if not self.grid[newLoc[0]][newLoc[1]] == DESTROYED:
                        destroyed = False;
                if destroyed and isContained:
                    return (HIT_DESTROYED, locs)
                
            return (HIT_SUCCESS, [])
        else:
            return (HIT_MISS, [])
    """
    Cette fonction est utilisee une seule fois mais le code est tellement moche que c'est deja trop.
    Elle sert a verifier si le 2nd joueur peut commencer a placer ses bateaux.
    """
    def should_switch(self):
        carrier_left = self.rules.get_boat_limit(BOAT_CARRIER) - self.carrier_placed
        battleship_left = self.rules.get_boat_limit(BOAT_BATTLESHIP) - self.battleship_placed
        cruiser_left = self.rules.get_boat_limit(BOAT_CRUISER) - self.cruiser_placed
        destroyer_left = self.rules.get_boat_limit(BOAT_DESTROYER) - self.destroyer_placed
        submarine_left = self.rules.get_boat_limit(BOAT_SUBMARINE) - self.submarine_placed
        return carrier_left <= 0 and battleship_left <= 0 and cruiser_left <= 0 and destroyer_left <= 0 and submarine_left <= 0
    """
    Pour savoir si on a gagne, il vaut mieux savoir s'il reste des bateaux a l'adversaire.
    Parce que si on ne sait pas, on peut pas gagner.
    """
    def has_boat_left(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] == BOAT:
                    return True
        return False
