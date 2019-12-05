import pygame
import copy
from Terrain import Terrain

class Map(object):
    # not sure if I need terrain object
    def __init__(self):
        self.line = []
        self.name = ""
    
    def draw(self, screen, scrollX, scrollY, game, terrain):
        for i in range(len(self.line)-1):
            x0, y0 = self.line[i]
            x1, y1 = self.line[i+1]
            x0 -= scrollX
            x1 -= scrollX
            y0 -= scrollY
            y1 -= scrollY
            distance = ((y0-y1)**2 + (x0-x1)**2)**0.5
            if distance < 25:
                if terrain:
                    pygame.draw.polygon(screen, (255, 255, 255), 
                        [(x0, y0), (x1, y1), (x1, game.height), (x0, game.height)])
                pygame.draw.line(screen, (0,0,0), (x0, y0), (x1, y1))