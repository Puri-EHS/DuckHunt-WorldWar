from constants import PLAY_BUTTON

import pygame

class Button:
    def __init__(self, _screen, _function_to_call):
        self.screen = _screen
        
        self.not_clicked_image = pygame.image.load(PLAY_BUTTON).convert_alpha()
        self.clicked_image = None
        self.rect = pygame.Rect((0, 0), (50, 50))
        
        self.current_image = self.not_clicked_image

        self.function_to_call = _function_to_call    

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False    
    
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def update(self, mouse_pos):
        if self.check_click(mouse_pos):
            self.current_image = self.clicked_image
            self.function_to_call()
        
        self.draw()