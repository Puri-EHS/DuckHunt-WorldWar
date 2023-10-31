
import pygame
import sys


def depth_movement(obj_depth, move_amount):
    obj_move = move_amount/obj_depth

    return obj_move

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Define colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rectangle Example")

# Rectangle 1
rect1_width = 200
rect1_height = 75
rect1_x = 400
rect1_y = 400

# Rectangle 2
rect2_width = 300
rect2_height = 125
rect2_x = 400
rect2_y = 500

# Rectangle 3
rect3_width = 300
rect3_height = 50
rect3_x = 200
rect3_y = 300

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)
    move_speed = 2
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        rect2_x += move_speed
        rect1_x += depth_movement(3, move_speed)
        rect3_x += depth_movement(5, move_speed)
    if keys[pygame.K_RIGHT]:
        rect2_x -= move_speed
        rect1_x -= depth_movement(3, move_speed)
        rect3_x -= depth_movement(5, move_speed)
    if keys[pygame.K_UP]:
        rect2_y += move_speed
        rect1_y += depth_movement(3, move_speed)
        rect3_y += depth_movement(5, move_speed)
    if keys[pygame.K_DOWN]:
        rect2_y -= move_speed
        rect1_y -= depth_movement(3, move_speed)
        rect3_y -= depth_movement(5, move_speed)

    # Draw rectangles
    pygame.draw.rect(screen, green, (rect3_x, rect3_y, rect3_width, rect3_height))
    pygame.draw.rect(screen, blue, (rect1_x, rect1_y, rect1_width, rect1_height))
    pygame.draw.rect(screen, red, (rect2_x, rect2_y, rect2_width, rect2_height))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

# Working on 3d method, which takes the depth of a image, and the amount moved, and decides how far to move
# the sprite/image to look like its at the proper depth

