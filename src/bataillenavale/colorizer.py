import pygame.surfarray


#Maximise le rouge d'un image.
def create_invalid (surface):
    #On recupere la totalite des pixels de l'image
    arr = pygame.surfarray.pixels3d(surface)
    #0 correspont au rouge
    arr[:,:,0] = 255
    
#Maximise le vert d'un image.
def create_selected (surface):
    #On recupere la totalite des pixels de l'image
    arr = pygame.surfarray.pixels3d(surface)
    #1 correspont au vert
    arr[:,:,1] = 255