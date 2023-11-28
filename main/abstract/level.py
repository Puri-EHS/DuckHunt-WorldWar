from abc import ABC, abstractmethod, abstractproperty
import pygame
from constants import LOBBY_MUSIC_PATH


class Level(ABC):
    
    def __init__(self, _name, _screen, _game_instance, _enemy_types=None):
        self.name = _name
        self.screen = _screen
        self.game_instance = _game_instance

        self.alive_enemies = []
        self.enemy_list = _enemy_types
        self.boss_enemy = None
        self.spawn_locations = [] # coordinates based on bushes / other foreground images

        self.bg_image = None
        self.bg_image_rect = None

        self.is_start_screen = False

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def ended(self) -> bool:
        pass
    
