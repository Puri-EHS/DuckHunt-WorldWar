from constants import VANILA_DUCK_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, USE_MOUSE

from abstract.enemy import Enemy
from abstract.enemy import AI
from sprite_sheet import Spritesheet
from sprite_sheet import Animation

import pygame   
import random

class VanilaDuck(Enemy):
    def __init__(self):
        self.sprite_sheet = Spritesheet(VANILA_DUCK_PATH)
        self.animation = Animation(self.sprite_sheet, 0, 0, 200, 200)
        self.ai = AI()
        self.ai.velocity = 4
        self.depth = 4.7
        self.world_coordinates = (self.ai.x, self.ai.y) 

        

        # Increase hit box if using controller: This is hardcoded, but needs to be a system. -AM
        if USE_MOUSE:
            self.rect = pygame.Rect(0, 0, 200, 200)
        else:
            self.rect = pygame.Rect(-42, -42, 84, 84)


        self.rect.center = self.world_coordinates

        self.health = 4

    def on_shot(self, _damage):
        self.health -= 1
        print(self.health)

        # new random location
        # Modified to not place below the half way mark or right at the top: -AM




    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)

    def update(self):
        self.ai.update()
        self.world_coordinates = (self.ai.x, self.ai.y)
