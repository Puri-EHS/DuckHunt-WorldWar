import pygame
import math
import numpy as np
from Spritesheet import Spritesheet

class PlayerGun:
    def __init__(self):

        self.crosshair = None

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


        self.cur_image = self.idle_images[1]

        self.size = (128*4, 120*4)

        self.bullets = []

        self.fov = 1/(20/180)

        self.angle = 0

        self.frames = 0

    def update(self):
        if pygame.mouse.get_pos()[0] < 800/3.0:
            self.gun_image_index = 0
        elif pygame.mouse.get_pos()[0] > 800/3.0 and pygame.mouse.get_pos()[0] < 800/3.0 * 2:
            self.gun_image_index = 1
        else:
            self.gun_image_index = 2

        # print(self.gun_image_index)

        #self.cur_image = self.idle_images[self.gun_image_index]

        self.frames += 1
        if(self.did_just_shoot and self.frames > 10):
            self.did_just_shoot = False
        elif not self.did_just_shoot:
            self.cur_image = self.idle_images[self.gun_image_index]

        # self.angle = abs((pygame.mouse.get_pos()[0]) / 800 * math.pi - math.pi)

    def render(self, screen):
        screen.blit(self.cur_image, (800/2-self.size[0]/2, 600-self.size[1]))


    def update_bullets(self, screen):
        for bullet in self.bullets:
            bullet.move()
            bullet.render(screen)


    def shoot(self, mousex, mousey):
        # velocity = np.array([(mousex - 400) / 800, (mousey - 600) / 600, 1])
        # bullet = Bullet(velocity[0] / self.fov, velocity[1] / self.fov, velocity[2], mousex, mousey, 0, 0)
        
        # #bullet = Bullet(velocity[0] * 5, velocity[1] * 5, velocity[2], mousex, mousey, 0, 0)
        # self.bullets.append(bullet)


        self.cur_image = self.shoot_images[self.gun_image_index]
        self.did_just_shoot = True
        self.frames = 0


class Bullet:

    def __init__(self, velx, vely, velz, initx, inity, bullet_drop, bullet_slowdown):
        self.dirx = velx
        self.diry = vely
        self.dirz = velz

        self.posx = initx
        self.posy = inity
        self.posz = .05

        self.speed = .025

        self.dirx *= self.speed
        self.diry *= self.speed
        self.dirz *= self.speed

        self.angle = 0

        self.bullet_drop = .015


    def move(self):
        self.diry += self.bullet_drop
        self.posx += self.dirx
        self.posy += self.diry 
        self.posz += self.dirz 

    def render(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.posx, self.posy), 5.0 / self.posz)


    

        
