from GameObject import GameObject
import pygame
import copy

class MainCharacter(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('tempBoard.png').convert_alpha()
        width, height = image.get_size()
        scaleImage = pygame.transform.scale(image, (int(width/20), int(height/20)))
        MainCharacter.baseImage = pygame.transform.rotate(scaleImage, -20)

    def __init__(self, cx, cy):
        image = copy.copy(MainCharacter.baseImage)
        super().__init__(cx, cy, image)
        self.isJumping = False
    
    def update(self):
        self.updateRect()
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(MainCharacter.baseImage, angle)