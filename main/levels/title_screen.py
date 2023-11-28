from abstract.level import Level
from constants import TITLE_SCREEN_PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from button import Button
import pygame

class TitleScreen(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)
        self.bg_image = pygame.image.load(TITLE_SCREEN_PATH).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.buttons = [
            Button(self.screen, self.game_instance.switch_to_level(0))
        ]

    def start(self):
        pass

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))

    def update(self):
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
        
        self.render()

    def stop(self):
        pass

    def ended(self):
        pass    
