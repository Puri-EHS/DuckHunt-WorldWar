from constants import VANILA_DUCK_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, USE_MOUSE

from abstract.enemy import Enemy
from abstract.enemy import AI
from sprite_sheet import Spritesheet
from sprite_sheet import Animation

import pygame   
import random
import numpy as np

class Parrot(Enemy):
    def __init__(self, game):
        super().__init__()
        self.sprite_sheet = Spritesheet(VANILA_DUCK_PATH)
        self.animation = Animation(self.sprite_sheet, 0, 0, 200, 200)
        self.ai = AI()
        self.ai.velocity = 8
        self.depth = 4.7
        self.world_coordinates = (self.ai.x, self.ai.y) 
        self.phase_2 = False

        self.ticks_per_hp_regen = 30
        self.current_ticks = 0
        

        self.rect = pygame.Rect(0, 0, 200, 200)
    
        self.rect.center = self.world_coordinates

        self.health = 150
        self.max_health = self.health

        self.player_ref = game.player

        
        self.random_std = .5

    def on_shot(self, _damage):
        self.health -= 10


    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)
        self.render_aim_line(_screen, _camera_offset)

    def update(self):
        
        self.enter_aim()
        self.aim()
        self.ai.update()
        self.world_coordinates = (self.ai.x, self.ai.y)
        if self.current_ticks >= self.ticks_per_hp_regen and self.health < self.max_health:
            self.current_ticks = 0
            self.health += 1
        else:
            self.current_ticks += 1

        ## Second stage triggers at hp < 30%
        if self.health < 50 and self.phase_2 != True:
            self.phase_2 = True
            self.ticks_per_hp_regen = 10000
            self.ai.velocity = 14
