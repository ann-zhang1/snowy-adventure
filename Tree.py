import pygame
import copy
from GameObject import GameObject

class Tree(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('tempTree.png').convert_alpha()
        width, height = image.get_size()
        Tree.baseImage = pygame.transform.scale(image, (int(width/20), int(height/20)))
    
    def __init__(self, cx, cy):
        image = copy.copy(Tree.baseImage)
        super().__init__(cx, cy, image)
    
    def update(self):
        self.updateRect()