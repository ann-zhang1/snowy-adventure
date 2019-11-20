import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, cx, cy, image):
        super().__init__()
        self.image = image
        self.width, self.height = image.get_size()
        self.cx, self.cy = cx, cy
        self.updateRect()

    def updateRect(self):
        self.rect = pygame.Rect(self.cx - self.width/2, self.cy - self.height/2, 
            self.width, self.height)