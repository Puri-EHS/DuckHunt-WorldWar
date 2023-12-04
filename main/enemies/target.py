from constants import TARGET_PATH, SCREEN_HEIGHT, SCREEN_WIDTH

from abstract.enemy import Enemy
from sprite_sheet import Spritesheet
from sprite_sheet import Animation

import pygame   

class Target(Enemy):
    def __init__(self):
        self.sprite_sheet = Spritesheet(TARGET_PATH)
        self.animation = Animation(self.sprite_sheet, 0, 0, 42, 42)

        self.depth = 4.7
        self.world_coordinates = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2) 

        self.rect = pygame.Rect(0, 0, 42, 42)
        self.rect.center = self.world_coordinates


    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)

    def update(self):
        pass