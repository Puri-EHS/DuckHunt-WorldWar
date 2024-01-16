import pygame

class Button:
    def __init__(self, _screen, center, not_clicked_image_path, clicked_image_path, _function_to_call, _args, _scale): # _args is a list of arguments
        self.screen = _screen
        #in the case of toggles,  Clicked and not clicked serve as a way to make toggle switches work... for example ON/OFF
        self.not_clicked_image = pygame.image.load(not_clicked_image_path).convert_alpha()
        self.not_clicked_image = pygame.transform.scale(self.not_clicked_image, (int(self.not_clicked_image.get_width() * _scale), int(self.not_clicked_image.get_height() * _scale)))
        
        self.clicked_image = pygame.image.load(clicked_image_path).convert_alpha()
        self.clicked_image = pygame.transform.scale(self.clicked_image, (int(self.clicked_image.get_width() * _scale), int(self.clicked_image.get_height() * _scale)))
        
        self.current_image = self.not_clicked_image
        self.rect = self.current_image.get_rect()
        self.rect.center = center

        self.function_to_call = _function_to_call   
        self.function_args = _args 
        
        self.last_state = False

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.last_state:
            self.last_state = pygame.mouse.get_pressed()[0]
            
            return True
        return False    
    
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def update(self, mouse_pos):
        if self.check_click(mouse_pos):
            if self.current_image == self.not_clicked_image:
                self.current_image = self.clicked_image
            elif self.current_image == self.clicked_image:
                self.current_image = self.not_clicked_image
            self.function_to_call(*self.function_args) # * is used to unpack the list of arguments
        self.last_state = pygame.mouse.get_pressed()[0]