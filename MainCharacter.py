from GameObject import GameObject
import pygame
import copy
import math

class MainCharacter(GameObject):
    @staticmethod
    def init():
        # image from cleanpng.com
        image = pygame.image.load('board.png').convert_alpha()
        width, height = image.get_size()
        MainCharacter.baseImage = pygame.transform.scale(image, (int(width/10), int(height/10)))

    def __init__(self, cx, cy, game):
        image = copy.copy(MainCharacter.baseImage)
        super().__init__(cx, cy, image)
        self.cx += self.width/2
        self.cy += self.height
        self.game = game
        self.jumpPower = 20
        self.reset()
    
    def reset(self):
        self.canRotate = False
        self.isRotating = False

        self.velX = 15
        self.velY = 0
        self.canJump = True

    def jump(self):
        thetaRadians = self.game.theta * math.pi / 180
        yJump = math.sin(math.pi/2 - thetaRadians)
        xJump = math.cos(math.pi/2 - thetaRadians)
        yChange = yJump * self.jumpPower
        xChange = xJump * self.jumpPower
        ySign = 1 if yChange >= 0 else -1
        xSign = 1 if xChange >= 0 else -1
        scaleY = ySign * abs(yChange * 2 ** 0.5)
        self.velX -= min(xSign * abs(xChange * 8) ** 0.5, 15)
        self.velY = -1 * (abs(yChange * 4) ** 0.5)
        print(self.velX)
    
    '''
    if False:
        if abs(xSign * (abs(xChange * 64) ** 0.5) > 15):
            self.velX = xSign * (abs(xChange * 64) ** 0.5)
        else:
            if xSign == 1:
                self.velX -= 5
            else: self.velX = 15
    else:
    '''
    
    def fall(self):
        self.velY += self.game.g
        self.velX -= 0.1 * (abs(self.velX)) ** 0.3

    def update(self):
        self.updateRect()
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(MainCharacter.baseImage, angle)
        self.width, self.height = self.image.get_size()