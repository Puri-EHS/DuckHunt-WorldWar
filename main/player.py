from constants import FPS, GUN, SCREEN_HEIGHT, SCREEN_WIDTH, SHOOT_SOUND_PATH

from sprite_sheet import Spritesheet

import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.gun = PlayerGun()

    def handle_input(self, _level_size):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move(-30, _level_size)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move(30, _level_size)
        if keys[pygame.K_SPACE]:
            self.gun.shoot()

    def move(self, _x, _level_size):
        self.x += _x

        if self.x >= _level_size/2:
            self.x = _level_size/2
        elif self.x <= -_level_size/2:
            self.x = -_level_size/2

    
    def update(self):
        pass

class PlayerGun:
    def __init__(self):
        self.max_ammo = 50000
        self.ammo_left = self.max_ammo

        self.reload_time = 2.5 * FPS
        self.shoot_time = .25 * FPS

        self.reload_timer = self.reload_time
        self.shoot_timer = self.shoot_time


        self.idle_images = []
        self.shoot_images = []
        self.idle_images.append(Spritesheet(GUN).image_at((128*2, 0, 128, 120)))
        self.idle_images[0] = pygame.transform.flip(self.idle_images[0], True, False)
        self.idle_images.append(Spritesheet(GUN).image_at((0, 0, 128, 120)))
        self.idle_images.append(Spritesheet(GUN).image_at((128*2, 0, 128, 120)))

        self.shoot_images.append(Spritesheet(GUN).image_at((128*4, 0, 128, 120)))
        self.shoot_images[0] = pygame.transform.flip(self.shoot_images[0], True, False)
        self.shoot_images.append(Spritesheet(GUN).image_at((128*3, 0, 128, 120)))
        self.shoot_images.append(Spritesheet(GUN).image_at((128*4, 0, 128, 120)))

        for i in range(len(self.idle_images)):
            self.idle_images[i] = pygame.transform.scale(self.idle_images[i],(128*4, 120*4))
            self.shoot_images[i] = pygame.transform.scale(self.shoot_images[i], (128*4, 120*4))

        self.cur_image = self.idle_images[1]
        self.image_size = (128*4, 120*4)

        self.gun_image_index = 1

        self.crosshair_coords = pygame.mouse.get_pos()


        self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
    

    def render(self, screen):
        screen.blit(self.cur_image, (SCREEN_WIDTH/2-self.image_size[0]/2, SCREEN_HEIGHT-self.image_size[1]))

    def update(self):
        self.crosshair_coords = pygame.mouse.get_pos()
        self.reload_timer += 1
        self.shoot_timer += 1


        if self.crosshair_coords[0] < 800/3:
            self.gun_image_index = 0
        elif self.crosshair_coords[0] > 800/3 and self.crosshair_coords[0] < 800/3*2:
            self.gun_image_index = 1
        else:
            self.gun_image_index = 2


        if self.reload_timer >= self.reload_time and self.ammo_left <= 0:
            self.ammo_left = self.max_ammo

        
        if self.shoot_timer >= self.shoot_time:
            self.cur_image = self.idle_images[self.gun_image_index]
            
        

    def can_shoot(self):
        return self.shoot_timer >= self.shoot_time and self.reload_timer >= self.reload_time

    def shoot(self):
        if self.ammo_left > 0 and self.can_shoot():
            self.ammo_left -= 1
            self.shoot_timer = 0

            # update image
            self.cur_image = self.shoot_images[self.gun_image_index]
            
            pygame.mixer.Sound.play(self.shoot_sound)
        
        if self.ammo_left <= 0:
            self.reload_timer = 0
            self.ammo_left = self.max_ammo

                