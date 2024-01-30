import globals
from globals import EAGLE_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, USE_MOUSE

from abstract.enemy import Enemy
from abstract.enemy import AI
from sprite_sheet import Spritesheet
from sprite_sheet import Animation

import pygame   
import random
import numpy as np

class Eagle(Enemy):
    def __init__(self, game):
        super().__init__()
        self.sprite_sheet = Spritesheet(EAGLE_PATH)
        self.animation = Animation(self.sprite_sheet, 0, 0, 200, 200)
        self.depth = 4.7
        self.ai = AI(500, 400, game.player, self.depth)
        self.ai.velocity = 450
        self.world_coordinates = (self.ai.x, self.ai.y) 
        self.phase_2 = False

        self.time_per_hp_regen = 1 # in seconds
        self.current_time = 0
        

        self.rect = pygame.Rect(0, 0, 200, 200)
    
        self.rect.center = self.world_coordinates

        self.health = 250
        self.max_health = self.health

        self.player_ref = game.player

        
        self.random_std = 0.25
        self.aim_enter_prob = 1/75
        self.shoot_time = 1.2 # in seconds


        if not USE_MOUSE[0]:
            self.aim_enter_prob = 1/75
            self.time_per_hp_regen = 1
            self.current_time = 0
            self.health = 200
            self.max_health = self.health
            self.shoot_time = 1.5 # in seconds

    def on_shot(self, _damage):
        super().on_shot(_damage)
        self.health -= 10


    def render(self, _screen, _camera_offset):
        self.depth_render(_screen, _camera_offset)
        self.render_aim_line(_screen, _camera_offset)
        super().render(_screen, _camera_offset)

    def update(self):
        super().update()


        self.enter_aim()
        self.aim()
        self.ai.update()
        self.world_coordinates = (self.ai.x, self.ai.y)
        if self.current_time >= self.time_per_hp_regen and self.health < self.max_health:
            self.current_time = 0
            self.health += 1
        else:
            self.current_time += globals.DELTA_TIME

        ## Second stage triggers at hp < 30%
        if self.health < 50 and self.phase_2 != True:
            self.phase_2 = True
            
