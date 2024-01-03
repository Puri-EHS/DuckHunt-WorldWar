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

        self.ticks_per_hp_regen = 30
        self.current_ticks = 0
        

        self.rect = pygame.Rect(0, 0, 200, 200)
    
        self.rect.center = self.world_coordinates

        self.health = 75
        self.max_health = self.health

    def on_shot(self, _damage):
        self.health -= 10
        print(self.health)

        # new random location
        # Modified to not place below the half way mark or right at the top: -AM




    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)

    def update(self):
        self.ai.update()
        self.world_coordinates = (self.ai.x, self.ai.y)
        if self.current_ticks >= self.ticks_per_hp_regen and self.health < self.max_health:
            self.current_ticks = 0
            self.health += 1
        else:
            self.current_ticks += 1
