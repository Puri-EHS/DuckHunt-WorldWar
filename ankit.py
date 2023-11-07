import pygame
import sys
from image_obj import image_object
import numpy as np
import math
from Gun import Gun


def depth_movement(obj_depth, move_amount):
    obj_move = move_amount/obj_depth

    return obj_move

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Image Move Example")
move_speed = 5

back_image = image_object("African-savannah-ecosystem.jpg", 2100, 900, 400, 300,5)
bush_image = image_object("dlf.pt-bush-png-29280.png", 2100, 450, 400, 550, 3)
backbush_image = image_object("dlf.pt-bush-png-29280.png", 2100, 200, 400, 300, 4)


gun = Gun()

shooting = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shooting = False
        
    # Clear the screen
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    # Update image position
    if keys[pygame.K_LEFT]:
        back_image.image_rect.x += depth_movement(back_image.depth, move_speed)
        bush_image.image_rect.x += depth_movement(bush_image.depth, move_speed)
        backbush_image.image_rect.x += depth_movement(backbush_image.depth, move_speed)
    if keys[pygame.K_RIGHT]:
        back_image.image_rect.x -= depth_movement(back_image.depth, move_speed)
        bush_image.image_rect.x -= depth_movement(bush_image.depth, move_speed)
        backbush_image.image_rect.x -= depth_movement(backbush_image.depth, move_speed)
    
    # Draw the image


    
    screen.blit(back_image.image, back_image.image_rect)
    screen.blit(backbush_image.image, backbush_image.image_rect)
    screen.blit(bush_image.image, bush_image.image_rect)

    gun.update ()
    gun.render(screen)

    if shooting:
        gun.shoot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    gun.update_bullets(screen)


    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()