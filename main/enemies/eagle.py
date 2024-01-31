import globals
from globals import EAGLE_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, USE_MOUSE

from abstract.enemy import Enemy
from abstract.enemy import AI
from sprite_sheet import Spritesheet
from sprite_sheet import Animation
import numpy

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
        self.ai.states[2].velocity = 400
        self.ai.states[0].velocity = 900
        self.ai.velocity = 800
        self.world_coordinates = (self.ai.x, self.ai.y) 
        self.phase_2 = False

        self.time_per_hp_regen = 0.3 # in seconds
        self.current_time = 0
        
        self.rect = pygame.Rect(0, 0, 200, 200)
    
        self.rect.center = self.world_coordinates

        self.health = 350
        self.max_health = self.health

        self.player_ref = game.player


        self.x_change = 1
        self.y_change = 1
        self.p = .6
        self.d = 3.0 
        self.xlasterror = 0
        self.ylasterror = 0
        self.random_multiplier = 5000
        self.random_mean = 0 # not used for this eagle
        self.random_std = 3
        self.aiming = False
        
        self.aim_coordinates = numpy.array([random.randrange(0, 1000), random.randrange(0, SCREEN_HEIGHT)])
        
        self.x_change_2 = 1
        self.y_change_2 = 1
        self.xlasterror_2 = 0
        self.ylasterror_2 = 0
        
        self.aim_coordinates_2 = numpy.array([random.randrange(0, 1000), random.randrange(0, SCREEN_HEIGHT)])


        self.aim_line_x_offset = -80
        self.aim_line_y_offset = 35

        self.aim_line_x_offset_2 = 80


        # Alex's way inferior code
        self.shoot_time = .5
        self.shoot_timer = 0
        self.firing = False

        self.hit_markers = []
        self.relative_hitmarker_position = (50, -50)
        
        self.random_std = 0.25
        self.aim_enter_prob = 1/15
        self.fire_enter_prob = 1/40
        self.shoot_time = .7 # in seconds



        if not USE_MOUSE[0]:
            self.aim_enter_prob = 1/30
            self.time_per_hp_regen = .5
            self.current_time = 0
            self.health = 350
            self.max_health = self.health
            self.fire_enter_prob = 1/60
            self.shoot_time = 1.1 # in seconds


    def render_aim_line(self, _screen, _camera_offset):
        if self.aiming:
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 4)
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset_2, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates_2[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates_2[1]), 4)

        elif self.firing:
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 4)
            pygame.draw.circle(_screen, (255, 0, 0), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 200 - (self.shoot_timer*(200/self.shoot_time)), 4)
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset_2, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates_2[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates_2[1]), 4)
            pygame.draw.circle(_screen, (255, 0, 0), (self.aim_coordinates_2[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates_2[1]), 200 - (self.shoot_timer*(200/self.shoot_time)), 4)


    def enter_aim(self):
        if not self.aiming and random.random() < self.aim_enter_prob and not self.firing:
            self.aiming = True
            
     
    def aim(self):
        if self.aiming:

            xerror = self.player_ref.x - self.aim_coordinates[0]
            yerror = SCREEN_HEIGHT/2 - self.aim_coordinates[1]
            xerrorchange = xerror - self.xlasterror
            yerrorchange = yerror - self.ylasterror
            self.xlasterror = xerror
            self.ylasterror = yerror

            xerror_2 = self.player_ref.x - self.aim_coordinates_2[0]
            yerror_2 = SCREEN_HEIGHT/2 - self.aim_coordinates_2[1]
            xerrorchange_2 = xerror_2 - self.xlasterror_2
            yerrorchange_2 = yerror_2 - self.ylasterror_2
            self.xlasterror_2 = xerror_2
            self.ylasterror_2 = yerror_2
             
            self.x_change += self.p * xerror + self.d * xerrorchange + self.random_multiplier * random.gauss(-.75, self.random_std) * globals.DELTA_TIME
            self.y_change += self.p * yerror + self.d * yerrorchange + self.random_multiplier * random.gauss(self.random_mean, self.random_std) * globals.DELTA_TIME

            # left and right aims have opposite means so that they aim apart

            self.x_change_2 += self.p * xerror_2 + self.d * xerrorchange_2 + self.random_multiplier * random.gauss(.75, self.random_std) * globals.DELTA_TIME
            self.y_change_2 += self.p * yerror_2 + self.d * yerrorchange_2 + self.random_multiplier * random.gauss(self.random_mean, self.random_std) * globals.DELTA_TIME

            self.aim_coordinates[0] += self.x_change * globals.DELTA_TIME
            self.aim_coordinates[1] += self.y_change * globals.DELTA_TIME

            self.aim_coordinates_2[0] += self.x_change_2 * globals.DELTA_TIME
            self.aim_coordinates_2[1] += self.y_change_2 * globals.DELTA_TIME

            if random.random() < 1/100:
                self.aiming = False
                self.firing = True

        if self.firing:
            self.shoot_timer += globals.DELTA_TIME
            
            if self.shoot_timer >= self.shoot_time:
                self.firing = False
                self.shoot_timer = 0
                self.pop_a_cap(self.aim_coordinates)
                self.pop_a_cap(self.aim_coordinates_2)
            


    def pop_a_cap(self, coords):
        if self.player_ref.coords[0] - coords[0] > -200 and self.player_ref.coords[0] - coords[0] < 200:
            if self.player_ref.coords[1] - coords[1] > -150 and self.player_ref.coords[1] - coords[1] < 150:
                if not self.player_ref.ducking and not self.player_ref.gun.pause_no_con:
                    self.player_ref.hp -= 100


    def get_screen_coordinates(self, _camera_offset):
        return (self.world_coordinates[0] - _camera_offset/self.depth, self.world_coordinates[1]) 

    def depth_render(self, _screen, _camera_offset):
        self.rect.center = self.get_screen_coordinates(_camera_offset)
        _screen.blit(self.animation.frames[self.animation.current_frame], self.rect.topleft)
     
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
            
