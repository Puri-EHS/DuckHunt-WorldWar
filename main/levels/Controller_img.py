from abstract.level import Level
from globals import SCREEN_HEIGHT, SCREEN_WIDTH, LOBBY_MUSIC_PATH, SPLASH_SCREEN_PATH, FPS
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

    def ended(self):
        if self.frame_counter >= 5:
            return True
        return False