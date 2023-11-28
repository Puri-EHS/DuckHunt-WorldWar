import pygame
import math
import numpy as np
from Spritesheet import Spritesheet
import constants
import random

class PlayerGun:
    def __init__(self):

        self.shoot_sound = pygame.mixer.Sound("shoot.mp3")

        self.crosshair = pygame.image.load("./crosshair.png").convert_alpha()
        self.crosshair_coords = (400, 300)
        self.cross_surf = pygame.Surface((self.crosshair.get_width(), self.crosshair.get_height()), pygame.SRCALPHA)
        self.cross_surf.blit(self.crosshair, (0,0))
        self.cross_surf = pygame.transform.scale(self.cross_surf, (30, 30))


        if not constants.USE_MOUSE:
            self.prev_crosshair_coords = self.crosshair_coords

        pygame.mouse.set_visible(False)
        #pygame.mouse.set_cursor(pygame.cursor.Cursor(self.cross_surf))

        self.idle_images = []
        self.shoot_images= []

        self.idle_images.append(Spritesheet("./gun.png").image_at((128*2, 0, 128, 120)))
        self.idle_images[0] = pygame.transform.flip(self.idle_images[0], True, False)
        self.idle_images.append(Spritesheet("./gun.png").image_at((0, 0, 128, 120)))
        self.idle_images.append(Spritesheet("./gun.png").image_at((128*2, 0, 128, 120)))

        self.shoot_images.append(Spritesheet("./gun.png").image_at((128*4, 0, 128, 120)))
        self.shoot_images[0] = pygame.transform.flip(self.shoot_images[0], True, False)
        self.shoot_images.append(Spritesheet("./gun.png").image_at((128*3, 0, 128, 120)))
        self.shoot_images.append(Spritesheet("./gun.png").image_at((128*4, 0, 128, 120)))


        for i in range(len(self.idle_images)):
            self.idle_images[i] = pygame.transform.scale(self.idle_images[i],(128*4, 120*4))
            self.shoot_images[i] = pygame.transform.scale(self.shoot_images[i], (128*4, 120*4))

        self.gun_image_index = 1
        self.did_just_shoot = False

        self.can_shoot = True

        self.reload_frame_time = 10
        self.shoot_frame_time = 10
        self.shoot_frames = 0

        self.max_ammo = 4
        self.ammo_left = self.max_ammo


        self.cur_image = self.idle_images[1]

        self.size = (128*4, 120*4)

        self.fov = 1/(20/180)

        self.gun_angle = 0

        self.prev_angle = 0
        self.angle = 0

    def update(self, queue, tix, tiy, tiz, nuckz, nucky, enemies):
        self.shoot_frames += 1

        if not constants.USE_MOUSE:
            if not queue.empty():
                tip, nuckle = queue.get() 

                self.prev_angle = self.angle
                if tiz.value - nuckz.value == 0:
                    self.angle = math.atan(0)
                else:
                    self.angle = math.atan((tiy.value - nucky.value)/ (tiz.value - nuckz.value)) * 180 / math.pi
                
                print(self.angle- self.prev_angle)

                # queue system could be the culprit for rare rapid shooting, but either way its kinda bad for this use case

                if tip is not None:
                    if self.did_just_shoot and self.shoot_frames > self.shoot_frame_time:
                        self.crosshair_coords = (800 - tix.value * 800, tiy.value * 600)
                        self.prev_crosshair_coords = self.crosshair_coords

                    if not self.did_just_shoot:
                        if self.angle - self.prev_angle > 14:
                            self.shoot(enemies)
                        else:
                            self.prev_crosshair_coords = self.crosshair_coords
                            self.crosshair_coords = (800 - tix.value * 800, tiy.value * 600)
                            if tiz.value - nuckz.value == 0:
                                self.angle = math.atan(0)
                            else:
                                self.angle = math.atan((tiy.value - nucky.value)/ (tiz.value - nuckz.value)) * 180 / math.pi
                
        else:
            self.crosshair_coords = pygame.mouse.get_pos()


        if self.crosshair_coords[0] < 800/3.0:
            self.gun_image_index = 0
        elif self.crosshair_coords[0] > 800/3.0 and self.crosshair_coords[0] < 800/3.0 * 2:
            self.gun_image_index = 1
        else:
            self.gun_image_index = 2


        
        if(self.did_just_shoot and self.shoot_frames > self.shoot_frame_time):
            self.did_just_shoot = False
        elif not self.did_just_shoot:
            self.cur_image = self.idle_images[self.gun_image_index]


    def render(self, screen):
        screen.blit(self.cur_image, (800/2-self.size[0]/2, 600-self.size[1]))
        screen.blit(self.cross_surf, (self.crosshair_coords[0]-self.cross_surf.get_width()/2, self.crosshair_coords[1]-self.cross_surf.get_height()/2))


    def shoot(self, enemies):
        self.cur_image = self.shoot_images[self.gun_image_index]
        self.did_just_shoot = True
        self.shoot_frames = 0
        pygame.mixer.Sound.play(self.shoot_sound)

        # basic collision detection - could use octree system later maybe - space partitioning
        for enemy in enemies:
            if enemy.x < self.crosshair_coords[0] < enemy.x + enemy.width:
                if enemy.y < self.crosshair_coords[1] < enemy.y + enemy.height:
                    enemy.x = random.randint(0, 800)
                    enemy.y = random.randint(0, 600)


                    


        



