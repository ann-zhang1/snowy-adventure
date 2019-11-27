from GameObject import GameObject
import pygame
import copy

class MainCharacter(GameObject):
    @staticmethod
    def init():
        # image from cleanpng.com
        image = pygame.image.load('board.png').convert_alpha()
        width, height = image.get_size()
        MainCharacter.baseImage = pygame.transform.scale(image, (int(width/10), int(height/10)))

    def __init__(self, cx, cy):
        image = copy.copy(MainCharacter.baseImage)
        super().__init__(cx, cy, image)
        self.cx += self.width/2
        self.cy += self.height
        self.reset()
    
    def reset(self):
        self.isJumping = False
        self.jumpHeight = 0
        self.jumpStage = 15

        self.isFalling = False
        self.isRotating = False
        self.fallStage = 0

    def jump(self):
        sign = 1
        if self.jumpStage < 0:
            sign = -1
        self.jumpHeight = sign * 0.1*(self.jumpStage)**2
        self.jumpStage -= 1
    
    def fall(self):
        self.fallHeight = -1 * 0.1*(self.fallStage)**2
        self.fallStage -= 1

    def resetJump(self):
        self.jumpHeight = 0
        self.jumpStage = 15
        self.isJumping = False

    def update(self):
        self.updateRect()
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(MainCharacter.baseImage, angle)
        self.width, self.height = self.image.get_size()