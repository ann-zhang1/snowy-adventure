import pygame
from Terrain import Terrain

class Map(object):
    # not sure if I need terrain object
    def __init__(self):
        self.line = []
        self.name = ""
    
    def draw(self, screen, scrollX):
        for i in range(len(self.line)-1):
            x0, y0 = self.line[i]
            x1, y1 = self.line[i+1]
            x0 -= scrollX
            x1 -= scrollX
            distance = ((y0-y1)**2 + (x0-x1)**2)**0.5
            if distance < 25:
                pygame.draw.line(screen, (0,0,0), (x0, y0), (x1, y1))