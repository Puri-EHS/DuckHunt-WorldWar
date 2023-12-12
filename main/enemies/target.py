from constants import TARGET_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, USE_MOUSE

from abstract.enemy import Enemy
from sprite_sheet import Spritesheet
from sprite_sheet import Animation

import pygame   
import random

class Target(Enemy):
    def __init__(self):
        self.sprite_sheet = Spritesheet(TARGET_PATH)
        self.animation = Animation(self.sprite_sheet, 0, 0, 42, 42)

        self.depth = 4.7
        self.world_coordinates = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2) 


        # Increase hit box if using controller: This is hardcoded, but needs to be a system. -AM
        if USE_MOUSE:
            self.rect = pygame.Rect(0, 0, 42, 42)
        else:
            self.rect = pygame.Rect(-42, -42, 84, 84)


        self.rect.center = self.world_coordinates

        self.health = 1

    def on_shot(self, _damage):
        self.health -= 0 # target is invincible

        # new random location
        # Modified to not place below the half way mark or right at the top: -AM
        self.world_coordinates = (random.randint(50, SCREEN_WIDTH), random.randint(50, SCREEN_HEIGHT/2))




    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)

    def update(self):
        pass