from abstract.level import Level
from globals import TITLE_SCREEN_PATH, SCREEN_HEIGHT, SCREEN_WIDTH,BACK_BUTTON, TOGGLE_OFF_BUTTON, TOGGLE_ON_BUTTON, PLAY_BUTTON
import globals
from button import Button
import pygame
import platform

def check_operating_system():
    return True

class OptionScreen(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)
        self.bg_image = pygame.image.load(TITLE_SCREEN_PATH).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if check_operating_system():
            self.buttons = [
                Button(self.screen, ((SCREEN_WIDTH/2) - 210, (SCREEN_HEIGHT/2) +290), BACK_BUTTON, BACK_BUTTON, self.game_instance.switch_to_level, [self.game_instance.current_level_index - 1], [], 2.5)
                #Use Mouse Toggles
                ,
                Button(self.screen, ((SCREEN_WIDTH/2) + 200, (SCREEN_HEIGHT/2) +50 ), TOGGLE_ON_BUTTON, TOGGLE_OFF_BUTTON, self.toggle_mouse,[], globals.USE_MOUSE ,2.5)

                ,Button(self.screen, ((SCREEN_WIDTH/2) + 200, (SCREEN_HEIGHT/2) -50 ), PLAY_BUTTON, PLAY_BUTTON, self.game_instance.update, [True], [], 2.5)
                #Hardcore mode toggles
                #,Button(self.screen, ((SCREEN_WIDTH/2) + 150, (SCREEN_HEIGHT/2) +150 ), TOGGLE_OFF_BUTTON, None, self.game_instance.switch_to_level, [self.game_instance.current_level_index + 1], 2.5)
            ]
        
        else:
            self.buttons = [
                Button(self.screen, ((SCREEN_WIDTH/2) - 210, (SCREEN_HEIGHT/2) +290), BACK_BUTTON, BACK_BUTTON, self.game_instance.switch_to_level, [self.game_instance.current_level_index - 1], [], 2.5)
                #Use Mouse Toggles
            ]
        self.game_level = False

    def start(self):
        print(__file__ + " " + self.name + " starting")

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        pygame.draw.line(self.screen, (100,100,100), (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2), 400)
        for button in self.buttons:
            button.draw()
        font = pygame.font.Font(None, 75)  # None uses the default font, 36 is the font size
        text_surface = font.render("Tracking Demo:", True, (255, 255, 255))  # Text color is white (RGB)
        self.screen.blit(text_surface, ((SCREEN_WIDTH/2) -350, (SCREEN_HEIGHT/2) -75 ))

        text_surface2 = font.render("Use Mouse:", True, (255, 255, 255))  # Text color is white (RGB)
        self.screen.blit(text_surface2, ((SCREEN_WIDTH/2) -250, (SCREEN_HEIGHT/2) +25 ))


    def update(self):
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
          

    def toggle_mouse(self):
        #this function changes the state of mouse:
        #this means when it is FALSE (OFF) it uses the tracker and TRUE (ON) to use the mouse
        globals.USE_MOUSE[0] = not globals.USE_MOUSE[0]
        print(globals.USE_MOUSE[0])
    
    def toggle_hardcore(self):
        pass

