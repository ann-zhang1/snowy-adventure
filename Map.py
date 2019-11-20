import pygame
from Terrain import Terrain

class Map(object):
    # not sure if I need terrain object
    def __init__(self):
        self.line = []
    
    def draw(self):
        pygame.draw.line(screen, (0,0,0), (900, 0), (900, 600), 5)