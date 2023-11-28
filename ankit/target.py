import pygame
class Target:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load("./target.png").convert_alpha()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


    
    