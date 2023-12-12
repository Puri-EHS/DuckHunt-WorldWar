from abstract.level import Level
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, LOBBY_MUSIC_PATH, SPLASH_SCREEN_PATH, FPS
import pygame

class Cont_img(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)
        self.bg_image = pygame.image.load('assets/ui/Controller_image.png').convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.frame_counter = 0
        self.game_level = False

    def start(self):
        print(__file__ + " " + self.name + " starting")
    

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))

    def update(self):
        self.frame_counter += 1

    def stop(self):
        del self

    def ended(self):
        if self.frame_counter >= 10 * FPS:
            return True
        return False