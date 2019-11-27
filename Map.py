import pygame
import copy
from Terrain import Terrain

class Map(object):
    # not sure if I need terrain object
    def __init__(self):
        self.line = []
        self.name = ""
    
    '''
    def extend(self):
        moreLine = copy.copy(self.line)
        moreLine = moreLine[::-1]
        newLine = []
        shift = self.line[-1][0] - self.line[0][0]
        for i in range(len(self.line)):
            cx = int(moreLine[i][0] + shift)
            cy = moreLine[i][1]
            print(cx, cy)
            newLine += [(cx, cy)]
        self.line += newLine
    '''
    
    def draw(self, screen, scrollX, game, terrain):
        for i in range(len(self.line)-1):
            x0, y0 = self.line[i]
            x1, y1 = self.line[i+1]
            x0 -= scrollX
            x1 -= scrollX
            distance = ((y0-y1)**2 + (x0-x1)**2)**0.5
            if distance < 25:
                if terrain:
                    pygame.draw.polygon(screen, (255, 255, 255), 
                        [(x0, y0), (x1, y1), (x1, game.height), (x0, game.height)])
                pygame.draw.line(screen, (0,0,0), (x0, y0), (x1, y1))