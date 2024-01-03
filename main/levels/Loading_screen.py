from abstract.level import Level
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, LOBBY_MUSIC_PATH, LOADING_SCREEN_PATH, FPS
import pygame

class LoadingScreen(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)
        self.bg_image = pygame.image.load(LOADING_SCREEN_PATH).convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH*1.5, SCREEN_HEIGHT))

        self.frame_counter = 0
        self.game_level = False

    def start(self):
        print(__file__ + " " + self.name + " starting")
        pygame.mixer.music.load(LOBBY_MUSIC_PATH)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    def render(self):
        self.screen.blit(self.bg_image, (0, 0))

    def update(self):
        self.frame_counter += 1

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        del self

    def ended(self):
        if self.frame_counter >= 10 * FPS:
            return True
        return False