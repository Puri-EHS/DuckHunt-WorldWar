import pygame
from TestCharacter import dude
#testing logic for movement of ducks

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
move_speed = 5

# Main game loop
running = True
MyGuy = dude(400, 300)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    MyGuy.update()
    screen.fill((0, 0, 0))
    MyGuy.draw(screen)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()