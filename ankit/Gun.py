import pygame
import math
import numpy as np
from Spritesheet import Spritesheet
class Gun:
    def __init__(self):

        self.image = Spritesheet("./gun.png").image_at((0, 0, 128, 120))
        self.image = pygame.transform.scale(self.image,(128*4, 120*4))

        self.shoot_image = Spritesheet("./gun.png").image_at((128*3, 0, 128, 120))
        self.shoot_image = pygame.transform.scale(self.shoot_image,(128*4, 120*4))

        self.cur_image = self.image

        self.size = (128*4, 120*4)

        self.bullets = []

        self.fov = 1/(20/180)

        self.angle = 0

        self.frames = 0

    def update(self):
        self.angle = abs((pygame.mouse.get_pos()[0]) / 800 * math.pi - math.pi)

    def render(self, screen):
        #pygame.draw.line(screen, (0,0,0), (400, 600), (400 + math.cos(self.angle)*50, 600 - math.sin(self.angle)*50), 5)
        screen.blit(self.cur_image, (800/2-self.size[0]/2, 600-self.size[1]))
        self.frames += 1
        if(self.cur_image == self.shoot_image and self.frames > 10):
            self.cur_image = self.image

    def update_bullets(self, screen):
        print(len(self.bullets))
        for bullet in self.bullets:
            bullet.move()
            bullet.render(screen)


    def shoot(self, mousex, mousey):
        # velocity = np.array([(mousex - 400) / 800, (mousey - 600) / 600, 1])
        # bullet = Bullet(velocity[0] / self.fov, velocity[1] / self.fov, velocity[2], mousex, mousey, 0, 0)
        
        # #bullet = Bullet(velocity[0] * 5, velocity[1] * 5, velocity[2], mousex, mousey, 0, 0)
        # self.bullets.append(bullet)


        self.cur_image = self.shoot_image
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


    

        
