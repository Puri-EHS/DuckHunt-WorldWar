#this is just for Nathan (me) to experiment and fool around with some code 

import pygame
import sys
from image_obj import image_object
import time
from Gun import Gun

#code for start screen

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = image_object("Images/Environments/Duck Hunt Savanna-1.png.png", 1536,790,400,300,5)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(background_image.image, background_image.image_rect)
    
    pygame.display.update()