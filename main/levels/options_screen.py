from abstract.level import Level
from constants import TITLE_SCREEN_PATH, SCREEN_HEIGHT, SCREEN_WIDTH,BACK_BUTTON, TOGGLE_OFF_BUTTON, TOGGLE_ON_BUTTON
from button import Button
import pygame

class OptionScreen(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)
        self.bg_image = pygame.image.load(TITLE_SCREEN_PATH).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        
        self.buttons = [
            Button(self.screen, ((SCREEN_WIDTH/2) - 210, (SCREEN_HEIGHT/2) +290), BACK_BUTTON, BACK_BUTTON, self.game_instance.switch_to_level, [self.game_instance.current_level_index - 1], 2.5)
            #Use Mouse Toggles
            ,Button(self.screen, ((SCREEN_WIDTH/2) + 150, (SCREEN_HEIGHT/2) +150 ), TOGGLE_OFF_BUTTON, TOGGLE_ON_BUTTON, self.toggle_mouse, [], 2.5)
            #Hardcore mode toggles
            #,Button(self.screen, ((SCREEN_WIDTH/2) + 150, (SCREEN_HEIGHT/2) +150 ), TOGGLE_OFF_BUTTON, None, self.game_instance.switch_to_level, [self.game_instance.current_level_index + 1], 2.5)
        ]

        self.game_level = False

    def start(self):
        print(__file__ + " " + self.name + " starting")

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        for button in self.buttons:
            button.draw()

    def update(self):
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())


    def stop(self):
        del self
        
    def toggle_mouse(self):
        pass
    
    def toggle_hardcore(self):
        pass

    def ended(self):
        pass    
