import pygame

from constants import FPS

class Spritesheet:
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert_alpha()
    
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        image.convert_alpha()

        return image
    
class Animation:
    def __init__(self, sheet_x_start, sheet_x_end, dimx, dimy):
        self.sprite_sheet = None
        self.current_frame = None
        self.frames = []
        for i in range(sheet_x_start, sheet_x_end + 1):
            self.frames.append(self.sprite_sheet.image_at((i * dimx, 0, dimx, dimy)))
        
        self.interval_time = .25 * FPS