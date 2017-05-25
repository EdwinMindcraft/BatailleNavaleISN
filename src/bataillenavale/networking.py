import socket
from bataillenavale.engine import HIT_SUCCESS, NULL, HIT_MISS, HIT_DESTROYED,\
    BOAT, DESTROYED, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT,\
    DIRECTION_RIGHT, Player, PLAYER_2, PLAYER_1
from threading import Thread

DEFAULT_PORT = 32500 # Port pour le serveur, completement arbitraire.

class Deserializer(Thread):
    """
    La classe Thread permet de faire tourner plusieurs processus en meme temps.
    Ici, on doit avoir un processus cote client pour obtenir les donnes du jeu par le reseau.
    Mais vu que l'on ne sait pas quand on recois ces donnes, on utilise un processus separe pour eviter que le jeu bug.
    """
    def __init__(self, client, instance, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.client = client
        self.instance = instance
        self._killed = False
    
    def run(self):
        while not self._killed:
            text = self.client.recv(32768)
            print(':'.join(hex(x) for x in text))
            deserialize(text, self.instance)
            
    def kill(self):
        self._killed = True
            

def createServer():
    server = socket.socket()
    host = socket.gethostname()
    server.bind((host, DEFAULT_PORT))
    server.listen(5)
    return server

def searchClient(server, instance):
    client, addr = server.accept()
    print ("Initialisation de la connection avec", addr)
    instance.thread = Deserializer(client, instance)
    instance.thread.start()
    return client

def initClientConnection(host, instance):
    client = socket.socket()
    client.connect((host, DEFAULT_PORT))
    instance.thread = Deserializer(client, instance)
    instance.thread.start()
    return client

def _intToString(val):
    """
    Cette fonction permet de transformer un objet int (entier) en un objet string (texte) de 4 caracteres.
    On a besoin de connaitre la taille de l'objet pour pouvoir le resortir plus tard.
    """
    text = ""
    text += chr(val & 0x0000000F)
    text += chr((val & 0x000000F0) >> 4)
    text += chr((val & 0x00000F00) >> 8)
    text += chr((val & 0x0000F000) >> 12)
    text += chr((val & 0x000F0000) >> 16)
    text += chr((val & 0x00F00000) >> 20)
    text += chr((val & 0x0F000000) >> 24)
    text += chr((val & 0xF0000000) >> 28)
    return text

def _boatPosToString(val):
    text = _intToString(len(val))
    for pos in val:
        location = pos[0]
        direction = pos[1]
        text += chr(location[0])
        text += chr(location[1])
        dirValue = 0
        if direction == DIRECTION_UP:
            dirValue = 0
        elif direction == DIRECTION_DOWN:
            dirValue = 1
        elif direction == DIRECTION_LEFT:
            dirValue = 2
        elif direction == DIRECTION_RIGHT:
            dirValue = 3
        text += chr(dirValue)
    print ("Boat using", len(text), "bytes")
    return text

def serialize(instance):
    text = _intToString(instance.rules.carrier_count)
    text += _intToString(instance.rules.battleship_count)
    text += _intToString(instance.rules.cruiser_count)
    text += _intToString(instance.rules.submarine_count)
    text += _intToString(instance.rules.destroyer_count)
    text += serializePlayer(instance.player_1)
    text += serializePlayer(instance.player_2)
    b = 0
    if instance.is_placing:
        b |= 0x1
    if instance.turn == PLAYER_2:
        b |= 0x2
    text += chr(b)
    print(':'.join(hex(x.encode()[0]) for x in text))
    return text.encode()

def deserialize(rawBytes, instance):
    abyte = []
    for b in rawBytes:
        abyte.append(b)
    instance.rules.carrier_count = _extractIntFromBytes(abyte)
    instance.rules.battleship_count = _extractIntFromBytes(abyte)
    instance.rules.cruiser_count = _extractIntFromBytes(abyte)
    instance.rules.submarine_count = _extractIntFromBytes(abyte)
    instance.rules.destroyer_count = _extractIntFromBytes(abyte)
    instance.player_1 = deserializePlayer(abyte)
    instance.player_2 = deserializePlayer(abyte)
    if abyte[0] & 0x1 == 0x1:
        instance.is_placing = True
    else:
        instance.is_placing = False
    if abyte[0] & 0x2 == 0x2:
        instance.turn = PLAYER_2
    else:
        instance.turn = PLAYER_1
    
"""
Genere un texte illisible pour l'homme contenant toute les informations sur un joueur
"""
def serializePlayer(player):
    text = ""
    charUsed = 0
    char = 0
    for rows in player.opponent_grid:
        for num in rows:
            digit = 0
            if num == NULL:
                digit = 0
            elif num == HIT_MISS:
                digit = 1
            elif num == HIT_SUCCESS:
                digit = 2
            elif num == HIT_DESTROYED:
                digit = 3
            
            char = char | (digit << (charUsed * 2))
            charUsed += 1
            if charUsed > 1:
                text += chr(char)
                charUsed = 0
                char = 0
    text += chr(char)
    char = 0
    charUsed = 0
    print ("Used", len(text), "bytes")
    
    for rows in player.grid:
        for num in rows:
            digit = 0
            if num == NULL:
                digit = 0
            elif num == BOAT:
                digit = 1
            elif num == DESTROYED:
                digit = 2
            
            char = char | (digit << (charUsed * 2))
            charUsed += 1
            if charUsed > 1:
                text += chr(char)
                charUsed = 0
                char = 0
    
    text += chr(char)
    char = 0
    charUsed = 0
    
    text += _intToString(player.rules.carrier_count)
    text += _intToString(player.rules.battleship_count)
    text += _intToString(player.rules.cruiser_count)
    text += _intToString(player.rules.submarine_count)
    text += _intToString(player.rules.destroyer_count)
    
    text += _intToString(player.carrier_placed)
    text += _intToString(player.battleship_placed)
    text += _intToString(player.cruiser_placed)
    text += _intToString(player.submarine_placed)
    text += _intToString(player.destroyer_placed)
    
    text += _boatPosToString(player.carrier_pos)
    text += _boatPosToString(player.battleship_pos)
    text += _boatPosToString(player.cruiser_pos)
    text += _boatPosToString(player.submarine_pos)
    text += _boatPosToString(player.destroyer_pos)
    
    return text

def _extractIntFromBytes(abyte):
    print (abyte[0], abyte[1], abyte[2], abyte[3], abyte[4], abyte[5], abyte[6], abyte[7])
    i = abyte[0] | (abyte[1] << 4) | (abyte[2] << 8) | (abyte[3] << 12) | (abyte[4] << 16) | (abyte[5] << 20) | (abyte[6] << 24) | (abyte[7] << 28)
    del abyte[0]
    del abyte[0]
    del abyte[0]
    del abyte[0]
    del abyte[0]
    del abyte[0]
    del abyte[0]
    del abyte[0]
    return i

def _extractBoatPosFromBytes(abyte):
    count = _extractIntFromBytes(abyte)
    print("Count :", count)
    ls = []
    for i in range(count):
        locX = abyte[0]
        locY = abyte[1]
        rawDir = abyte[2]
        del abyte[0]
        del abyte[0]
        del abyte[0]
        location = (locX, locY)
        direction = 0
        if rawDir == 0:
            direction = DIRECTION_UP
        elif rawDir == 1:
            direction = DIRECTION_DOWN
        elif rawDir == 2:
            direction = DIRECTION_LEFT
        elif rawDir == 3:
            direction = DIRECTION_RIGHT
        print (i, (location, direction))
        ls.append((location, direction))
    return ls

def deserializePlayer(abyte):
    player = Player()
    sz = len(abyte)
    charUsed = 0
    for rows in range(10):
        for num in range(10):
            byte = abyte[0] & (0x3 << (2 * charUsed))
            print(byte)
            state = NULL
            if byte == 0:
                state = NULL
            elif byte == 1:
                state = HIT_MISS
            elif byte == 2:
                state = HIT_SUCCESS
            elif byte == 3:
                state = HIT_DESTROYED
            player.opponent_grid[rows][num] = state
            charUsed += 1
            if charUsed > 1:
                del abyte[0]
                charUsed = 0
                
    del abyte[0]
    charUsed = 0
    print ("Used", sz - len(abyte), "bytes")
    
    for rows in range(10):
        for num in range(10):
            byte = abyte[0] & (0x3 << (2 * charUsed))
            state = NULL
            if byte == 0:
                state = NULL
            elif byte == 1:
                state = BOAT
            elif byte == 2:
                state = DESTROYED
            player.grid[rows][num] = state
            charUsed += 1
            if charUsed > 1:
                del abyte[0]
                charUsed = 0
                
    del abyte[0]
    charUsed = 0
    print (len(abyte), "bytes remaining...")
    player.rules.carrier_count = _extractIntFromBytes(abyte)
    player.rules.battleship_count = _extractIntFromBytes(abyte)
    player.rules.cruiser_count = _extractIntFromBytes(abyte)
    player.rules.submarine_count = _extractIntFromBytes(abyte)
    player.rules.destroyer_count = _extractIntFromBytes(abyte)
    
    player.carrier_placed = _extractIntFromBytes(abyte)
    player.battleship_placed = _extractIntFromBytes(abyte)
    player.cruiser_placed = _extractIntFromBytes(abyte)
    player.submarine_placed = _extractIntFromBytes(abyte)
    player.destroyer_placed = _extractIntFromBytes(abyte)
    
    player.carrier_pos = _extractBoatPosFromBytes(abyte)
    player.battleship_pos = _extractBoatPosFromBytes(abyte)
    player.cruiser_pos = _extractBoatPosFromBytes(abyte)
    player.submarine_pos = _extractBoatPosFromBytes(abyte)
    player.destroyer_pos = _extractBoatPosFromBytes(abyte)
    
    return player