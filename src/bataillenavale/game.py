from bataillenavale import engine, networking
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
        self.is_placing = True
        self.locked = False
        self.turn = engine.PLAYER_1
        self.selected_boat_type = BOAT_CARRIER
        self.grid_scale = grid_scale
        self.enable_borders = enable_borders
        self.local = True
        self.is_host = True
        self.server = None
        self.client = None
        self.thread = None
        self.victor = NULL
    
    def initHost(self):
        self.server = networking.createServer()
        self.local = False
        self.client = networking.searchClient(self.server, self)
    
    def initClient(self, host):
        self.client = networking.initClientConnection(host, self)
        self.local = False
        self.is_host = False
    
    """
    Est-ce que quelqu'un a gagne ?
    """
    def check_win(self):
        if self.player_1.has_boat_left() and not self.player_2.has_boat_left():
            self.victor = PLAYER_1
        elif not self.player_1.has_boat_left() and self.player_2.has_boat_left():
            self.victor = PLAYER_2
    """
    Quel joueur est en train de jouer ?
    """
    def get_current_player(self):
        return self.player_1 if self.turn == PLAYER_1 else self.player_2
    
    """
    Quelle est la taille de tel ou tel bateau ?
    """
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
    """
    Cette fonction permet de definir de maniere "controlle" la taille de la grille.
    Dans d'autre language, toutes les variables ne sont pas visibles de tout le monde.
    """
    def set_grid_size(self, size):
        self.grid_scale = size
    """
    On change la rotation de placement.
    """
    def cycle_rotation(self):
        if (self.rotation == DIRECTION_DOWN):
            self.rotation = DIRECTION_LEFT
        elif (self.rotation == DIRECTION_LEFT):
            self.rotation = DIRECTION_UP
        elif (self.rotation == DIRECTION_UP):
            self.rotation = DIRECTION_RIGHT
        else:
            self.rotation = DIRECTION_DOWN
    """
    Donne la case a partir de deux acces a cette methode (un pour X, un pour Y)
    """
    def snap(self, num):
        size = self.grid_scale / (11 if self.enable_borders else 10)
        return floor(num / size) - (1 if self.enable_borders else 0)
    """
    Meme chose qu'au-dessus, sauf que c'est la position sur l'ecran de la case a la place.
    """
    def render_snap(self, num):
        size = self.grid_scale / (11 if self.enable_borders else 10)
        return int(floor(num / size) * (size + (1 if self.enable_borders else 0)))
    """
    Taille d'une case.
    """
    def cube_size(self):
        return int(self.grid_scale / (11 if self.enable_borders else 10))
    
    """
    Est-ce que le joueur actif peut placer un bateau ?
    """
    def can_place_boat(self, boat_type, mouse_x, mouse_y):
        x = self.snap(mouse_x)
        y = self.snap(mouse_y)
        if (x < 0 or x > 9):
            return False
        if (y < 0 or y > 9):
            return False
        return self.get_current_player().can_place_boat_at((x, y), boat_type, self.rotation)
    """
    Gere ce qu'il se passe lorsque que l'on clique la fenetre.
    Soit on peut selectionner un bateau.
    Soit on peut placer un bateau.
    Soit on peut tirer sur une case.
    """
    def handle_play(self, mouse_x, mouse_y):
        if (self.locked):
            return
        if (mouse_x > self.boat_selector_pos[0] and mouse_x < self.boat_selector_pos[0] + 1020 and mouse_y + 60 > self.boat_selector_pos[1] and mouse_y < self.boat_selector_pos[1] + 200):
            pos_x = mouse_x - self.boat_selector_pos[0] + 10
            pos_y = mouse_y - self.boat_selector_pos[1] + 60
            if (pos_x > 10 and pos_x < 235):
                if (pos_y > 10 and pos_y < 55):
                    self.selected_boat_type = BOAT_CARRIER
                elif (pos_y > 65 and pos_y < 120):
                    self.selected_boat_type = BOAT_BATTLESHIP
                elif (pos_y > 130 and pos_y < 185):
                    self.selected_boat_type = BOAT_CRUISER
            elif (pos_x > 510 and pos_x < 755):
                if (pos_y > 10 and pos_y < 55):
                    self.selected_boat_type = BOAT_SUBMARINE
                elif (pos_y > 65 and pos_y < 120):
                    self.selected_boat_type = BOAT_DESTROYER
            self.sync()
            return
        if (self.is_placing):
            self.place_boat_at(self.selected_boat_type, mouse_x, mouse_y)
            if (self.get_current_player().should_switch()):
                if (self.turn == PLAYER_1):
                    self.turn = PLAYER_2
                else:
                    self.turn = PLAYER_1
                    self.is_placing = False
            self.sync()
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
        self.check_win()
        if self.victor != NULL:
            self.locked = True
        if self.turn == PLAYER_1:
            self.turn = PLAYER_2
        else:
            self.turn = PLAYER_1
        self.sync()
            
    def sync(self):
        if not self.local and not self.client is None:
            self.client.send(networking.serialize(self))
            
    """
    Place un bateau pour le joueur actif
    """
    def place_boat_at(self, boat_type, mouse_x, mouse_y):
        x = self.snap(mouse_x)
        y = self.snap(mouse_y)
        if (x < 0 or x > 9):
            return False
        if (y < 0 or y > 9):
            return False
        if not self.can_place_boat(boat_type, mouse_x, mouse_y):
            return False
        self.get_current_player().place_boat((x, y), boat_type, self.rotation)
        return True
        