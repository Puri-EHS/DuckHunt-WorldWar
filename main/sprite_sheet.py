import pygame

class Spritesheet:
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert_alpha()
    
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        image.convert_alpha()
        #image.set_alpha(255)
        return image
    
class Animation:
    def __init__(self):
        pass