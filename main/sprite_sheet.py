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
    def __init__(self, sprite_sheet, tile_start, tile_end, dimx, dimy):
        self.sprite_sheet = sprite_sheet
        self.frames = []
        for i in range(tile_start, tile_end + 1):
            self.frames.append(self.sprite_sheet.image_at((i * dimx, 0, dimx, dimy)))
        
        self.current_frame = 0

        self.interval_timer = 0
        self.interval_time = .25 * FPS


    
    def update(self):
        self.interval_timer += 1
        if self.interval_timer >= self.interval_time:
            self.interval_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0