import pygame
import math
import numpy as np
from Spritesheet import Spritesheet
import constants

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

        self.idle_images.append(Spritesheet("ankit/gun.png").image_at((128*2, 0, 128, 120)))
        self.idle_images[0] = pygame.transform.flip(self.idle_images[0], True, False)
        self.idle_images.append(Spritesheet("ankit/gun.png").image_at((0, 0, 128, 120)))
        self.idle_images.append(Spritesheet("ankit/gun.png").image_at((128*2, 0, 128, 120)))

        self.shoot_images.append(Spritesheet("ankit/gun.png").image_at((128*4, 0, 128, 120)))
        self.shoot_images[0] = pygame.transform.flip(self.shoot_images[0], True, False)
        self.shoot_images.append(Spritesheet("ankit/gun.png").image_at((128*3, 0, 128, 120)))
        self.shoot_images.append(Spritesheet("ankit/gun.png").image_at((128*4, 0, 128, 120)))


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

        self.bullets = []

        self.fov = 1/(20/180)

        self.angle = 0


    def update(self, queue):
        self.shoot_frames += 1
        if not constants.USE_MOUSE:
            if not queue.empty():
                tip, nuckle = queue.get() 
                # queue system could be the culprit for rare rapid shooting, but either way its kinda bad for this use case

                if tip is not None:
                    
                    if self.did_just_shoot and self.shoot_frames > self.shoot_frame_time:
                        self.crosshair_coords = (800 - tip.x * 800, tip.y * 600)
                        self.prev_crosshair_coords = self.crosshair_coords


                    
                    if not self.did_just_shoot:
                        if self.crosshair_coords[1] - tip.y * 600 > 100:
                            self.shoot()
                        else:
                            self.prev_crosshair_coords = self.crosshair_coords
                            self.crosshair_coords = (800 - tip.x * 800, tip.y * 600)

                
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
        screen.blit(self.cross_surf, self.crosshair_coords)

    def update_bullets(self, screen):
        for bullet in self.bullets:
            bullet.move()
            bullet.render(screen)

    def shoot(self):
        self.cur_image = self.shoot_images[self.gun_image_index]
        self.did_just_shoot = True
        self.shoot_frames = 0
        pygame.mixer.Sound.play(self.shoot_sound)

        



