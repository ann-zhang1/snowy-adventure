import pygame
import copy
from GameObject import GameObject

class Tree(GameObject):
    @staticmethod
    def init():
        # image from www.jing.fm
        image = pygame.image.load('tempTree.png').convert_alpha()
        width, height = image.get_size()
        Tree.baseImage = pygame.transform.scale(image, (int(width/10), int(height/10)))
    
    def __init__(self, cx, cy):
        image = copy.copy(Tree.baseImage)
        super().__init__(cx, cy, image)
        self.originalX = cx
        self.cy -= self.height/2
        self.originalY = self.cy
    
    def fixX(self, scroll):
        self.cx = self.originalX - scroll
    
    def fixY(self, scroll):
        self.cy = self.originalY - scroll
    
    def update(self):
        self.updateRect()