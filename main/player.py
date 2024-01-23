from constants import FPS, GUN, CROSSHAIR, CONNOTFOUND, SCREEN_HEIGHT, SCREEN_WIDTH, SHOOT_SOUND_PATH, USE_MOUSE
import constants
from sprite_sheet import Spritesheet
from image_object import ImageObj


from physical_gun_detection import Tracker

import pygame

class Player:
    def __init__(self, _game_instance):
        self.x = 0
        self.coords = [self.x, SCREEN_HEIGHT/2]
        self.gun = PlayerGun()
        self.game_instance = _game_instance
        self.ducking = False
        self.ducking_kick_timer = 0
        self.ducking_kick_max = 10
        self.hp = 100

    def handle_input(self, _level_size):
        keys = pygame.key.get_pressed()
        
        if constants.USE_MOUSE[0]:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.move(-30 if not self.ducking else -10, _level_size)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.move(30 if not self.ducking else 10, _level_size)
            if keys[pygame.K_SPACE] and self.gun.can_shoot() and not self.ducking:
                self.gun.shoot()
                self.game_instance.current_level.check_enemy_point_collisions(self.gun.crosshair_coords, self.gun.damage)
        
        # Allows lateral movement and firing with controler: move crosshairs to one side to move
        else:
            if keys[pygame.K_a] or keys[pygame.K_LEFT] or self.gun.crosshair_coords[0] <= 75:
                self.move(-30 if not self.ducking else -10, _level_size)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] or self.gun.crosshair_coords[0] >= 700:
                self.move(30 if not self.ducking else 10, _level_size)
            if (self.gun.tracker.num_fire >= 2 and self.gun.tracker.num_fire < 4) and self.gun.can_shoot() and not self.ducking:
                self.gun.shoot()
                self.game_instance.current_level.check_enemy_point_collisions(self.gun.crosshair_coords, self.gun.damage)
        
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not self.ducking:
            self.ducking = True
            print(self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.y)
            self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].scale(3)
            self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center = (self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center[0], self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center[1] - 1050)
            # print coords
            #print(self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.y)
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.ducking:
            self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].scale(1/3)
            #self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center = (self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center[0], self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center[1])
            #print(self.game_instance.current_level.foreground_images[len(self.game_instance.current_level.foreground_images)-1].image_rect.center)

            self.ducking = False
    
    def move(self, _x, _level_size):
        self.x += _x
        self.coords[0] += _x

        end = (_level_size/2 - SCREEN_WIDTH/2)*5
        if self.x >= end:
            self.x = end
            self.coords[0] = end
        elif self.x <= -end:
            self.x = -end
            self.coords[0] = -end

    
    def update(self):
        #print(self.x)
        pass

class PlayerGun:
    def __init__(self):
        self.x_offset = 384
        self.y_offset = 360
        self.max_ammo = 3000

        self.ammo_left = self.max_ammo

        self.gun_sprite_sheet = Spritesheet(GUN)

        self.damage = 1


        self.tracker = Tracker()
        self.tracker.track_icons()

        self.reload_time = 0
        self.shoot_time = 4 
        self.cooldown_time = 5

        self.reload_timer = self.reload_time
        self.shoot_timer = self.shoot_time
        self.cooldown_timer = self.cooldown_time

        # Limit how often tracking is called, as to improve fps
        self.frames_per_track = 2
        self.current_frames_untracked = 0

        self.idle_images = []
        self.shoot_images = []
        self.idle_images.append(self.gun_sprite_sheet.image_at((128*2, 0, 128, 120)))
        self.idle_images[0] = pygame.transform.flip(self.idle_images[0], True, False)
        self.idle_images.append(self.gun_sprite_sheet.image_at((0, 0, 128, 120)))
        self.idle_images.append(self.gun_sprite_sheet.image_at((128*2, 0, 128, 120)))

        self.shoot_images.append(self.gun_sprite_sheet.image_at((128*4, 0, 128, 120)))
        self.shoot_images[0] = pygame.transform.flip(self.shoot_images[0], True, False)
        self.shoot_images.append(self.gun_sprite_sheet.image_at((128*3, 0, 128, 120)))
        self.shoot_images.append(self.gun_sprite_sheet.image_at((128*4, 0, 128, 120)))

        for i in range(len(self.idle_images)):
            self.idle_images[i] = pygame.transform.scale(self.idle_images[i],(128*4, 120*4))
            self.shoot_images[i] = pygame.transform.scale(self.shoot_images[i], (128*4, 120*4))

        self.cur_image = self.idle_images[1]
        self.image_size = (128*4, 120*4)

        self.gun_image_index = 1

        #Hardcoded to work with tracking. WIll make it listen to constants 
        if not constants.USE_MOUSE[0]:
            self.crosshair_coords = self.tracker.stable_avg_x, self.tracker.stable_avg_y
        else:
            self.crosshair_coords = pygame.mouse.get_pos()

        self.crosshair_img = pygame.image.load(CROSSHAIR)
        self.con_not_found_img = pygame.image.load(CONNOTFOUND)
        self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
        self.pause_no_con = False

    def render(self, screen):
        screen.blit(self.cur_image, (SCREEN_WIDTH/2-self.image_size[0]/2, SCREEN_HEIGHT-self.image_size[1]))
        screen.blit(self.crosshair_img, (self.crosshair_coords[0]-30, self.crosshair_coords[1]-30))
        if not constants.USE_MOUSE[0]:
            if self.tracker.num_fire > 8:
                screen.blit(self.con_not_found_img, (0, 0))
                print("con not found O_o")
                self.pause_no_con = True
            else:
                self.pause_no_con = False

    def update(self):
        
        if not constants.USE_MOUSE[0]:
            if self.current_frames_untracked < self.frames_per_track:
                self.current_frames_untracked += 1
            else:
                self.tracker.track_icons()
                self.current_frames_untracked = 0

            self.crosshair_coords = self.tracker.stable_avg_x, self.tracker.stable_avg_y
        else:
            self.crosshair_coords = pygame.mouse.get_pos()
        
        
        self.reload_timer += 1
        self.shoot_timer += 1
        self.cooldown_timer += 1

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
        
        # Set num of frames without controler detection needed to trigger fire
        #if not USE_MOUSE and self.tracker.num_fire >= 2 and self.tracker.num_fire < 4 and self.can_shoot():
         #   self.shoot()
        

    def can_shoot(self):
        return self.shoot_timer >= self.shoot_time and self.reload_timer >= self.reload_time and self.cooldown_timer > self.cooldown_time

    def shoot(self):
        if self.ammo_left > 0 and self.can_shoot():
            self.ammo_left -= 1
            self.shoot_timer = 0
            self.cooldown_timer = 0

            # update image
            self.cur_image = self.shoot_images[self.gun_image_index]
            
            #pygame.mixer.Sound.play(self.shoot_sound)
        
        if self.ammo_left <= 0:
            self.reload_timer = 0
            self.ammo_left = self.max_ammo

                