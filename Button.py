import pygame
import copy
from GameObject import GameObject

class Button(GameObject):
    @staticmethod
    def init():
        # image from hiclipart.com
        image = pygame.image.load('greyButton.png').convert_alpha()
        width, height = image.get_size()
        Button.baseImage = pygame.transform.scale(image, (int(width/7), int(height/7)))
    
    def __init__(self, cx, cy, text):
        image = copy.copy(Button.baseImage)
        super().__init__(cx, cy, image)
        self.text = text
    
    def clicked(self, x, y):
        x0 = self.cx - self.width/2
        y0 = self.cy - self.height/2
        x1 = self.cx + self.width/2
        y1 = self.cy + self.height/2
        return (x0 <= x <= x1) and (y0 <= y <= y1)
    
    def update(self):
        self.updateRect()