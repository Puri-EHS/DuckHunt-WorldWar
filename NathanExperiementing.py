#this is just for Nathan (me) to experiment and fool around with some code 

import pygame
import sys
from image_obj import image_object
import time
from Gun import Gun

#code for start screen
class Startscreen:
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600

    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    background_image = image_object("Images/Environments/DuckHuntMenuBackground.png", 800,600,400,300,5)
    title_image = image_object("Images/UI/DuckHuntTitle.png", 600, 400, 400, 200, 5)
    play_game_button = image_object("Images/UI/PlayButton.png", 218, 76, 425, 280, 4)
    options_button = image_object("Images/UI/OptionButton.png", 218, 76, 425, 376, 4)

    def play_button_clicked(screen):
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_game_button.image_rect.collidepoint(event.pos):
                    play_button_clicked(screen)
                    
        #builds the screen
        screen.blit(background_image.image, background_image.image_rect)
        screen.blit(title_image.image, title_image.image_rect)
        screen.blit(play_game_button.image, play_game_button.image_rect)
        screen.blit(options_button.image, options_button.image_rect)
        
        pygame.display.update()