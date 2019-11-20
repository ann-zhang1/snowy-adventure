import pygame

class Terrain(object):
    def __init__(self):
        self.line = []
    
    def draw(self):
        pygame.draw.line(screen, (0,0,0), (900, 0), (900, 600), 5)