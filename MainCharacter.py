from GameObject import GameObject
import pygame
import copy

class MainCharacter(GameObject):
    @staticmethod
    def init():
        image = pygame.image.load('board.png').convert_alpha()
        width, height = image.get_size()
        MainCharacter.baseImage = pygame.transform.scale(image, (int(width/10), int(height/10)))

    def __init__(self, cx, cy):
        image = copy.copy(MainCharacter.baseImage)
        super().__init__(cx, cy, image)
        self.isJumping = False
        self.cx -= self.width/2
        self.cy -= self.height
        self.jumpHeight = 0
        self.jumpStage = 0
    
    def jump(self):
        self.jumpStage += 1
        if self.jumpStage < 20:
            self.jumpHeight = 0.4*(self.jumpStage-10)**2 - 50
        else:
            self.jumpHeight = 0
            self.jumpStage = 0
            self.isJumping = False
    
    def update(self):
        self.updateRect()
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(MainCharacter.baseImage, angle)