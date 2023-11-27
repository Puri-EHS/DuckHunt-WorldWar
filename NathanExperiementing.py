#this is just for Nathan (me) to experiment and fool around with some code 

import pygame
import sys
from image_obj import image_object
import time
from Gun import Gun

#code for start screen
class Startscreen:
    
    def __init__(self):
        #When True use mouse, when false, use gestures
        self.mouse_toggle = True
        #Hardcore mode means if player dies, game restarts entirely, set to false on default
        self.hardcore_mode = False
        #volume control, false by default
        self.mute = False
        
    def start_screen(self): 
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
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_game_button.image_rect.collidepoint(event.pos):
                        self.play_button_clicked(screen)
                    if options_button.image_rect.collidepoint(event.pos):
                        self.option_button_clicked()
                    
            #builds the screen
            screen.blit(background_image.image, background_image.image_rect)
            screen.blit(title_image.image, title_image.image_rect)
            screen.blit(play_game_button.image, play_game_button.image_rect)
            screen.blit(options_button.image, options_button.image_rect)
            
            pygame.display.update()


    def play_button_clicked(screen):
        #call level 1
        color = (255, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))
    
    def option_button_clicked():
        #when button clicked, take player to screen with toggleable buttons
        #create toggle buttons (on/off)
        #when when clicked, switch to whatever it was not (true -> False) and update image, update variable
        pass

start = Startscreen()
start.start_screen()
