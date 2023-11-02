
import pygame
import sys
from image_obj import image_object
import time

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

all_image_objects = []

back_image = image_object("African-savannah-ecosystem.jpg", 2100,900,400,300,5)
all_image_objects.append(back_image)

backbush_image = image_object("dlf.pt-bush-png-29280.png", 2100, 200, 400, 300, 4)
all_image_objects.append(backbush_image)

bush_image = image_object("dlf.pt-bush-png-29280.png", 2100, 700, 400, 600, 2)
all_image_objects.append(bush_image)

# Main game loop
running = True
crouched = False
jump = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    # Update image position
    if keys[pygame.K_LEFT]:
        for image in all_image_objects:
            image.image_rect.x += depth_movement(image.depth, move_speed)
       
    if keys[pygame.K_RIGHT]:
        for image in all_image_objects:
            image.image_rect.x -= depth_movement(image.depth, move_speed)
    
    if keys[pygame.K_DOWN] and crouched == False:
        crouched = True
        for image in all_image_objects:
            image.image_rect.y -= depth_movement(image.depth, 500)
    
    if keys[pygame.K_UP] and crouched == True:
        crouched = False
        for image in all_image_objects:
            image.image_rect.y += depth_movement(image.depth, 500)


    # Draw the image
    for image in all_image_objects:
        screen.blit(image.image, image.image_rect)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()