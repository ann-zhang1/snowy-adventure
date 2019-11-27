import pygame
import copy
from GameObject import GameObject

class Rock(GameObject):
    @staticmethod
    def init():
        # image from myrealdomain.com
        image = pygame.image.load('tempRock.png').convert_alpha()
        width, height = image.get_size()
        Rock.baseImage = pygame.transform.scale(image, (int(width/20), int(height/20)))
    
    def __init__(self, cx, cy):
        image = copy.copy(Rock.baseImage)
        super().__init__(cx, cy, image)
    
    def update(self):
        self.updateRect()