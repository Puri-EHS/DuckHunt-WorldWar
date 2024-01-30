from abc import ABC, abstractmethod, abstractproperty
import pygame 
import globals
from globals import MUSIC_1

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

        self.images = [
            
        ]

        self.game_level = False

        self.is_over = False
        self.victory_deley = 1.5
        self.current_victory_timer = 0
        
        self.frame_counter = 0

    def start(self):
        pygame.mixer.music.load(MUSIC_1)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    
    def depth_render(self, _image_list, _offset):
        for image_obj in _image_list:
            self.screen.blit(image_obj.image, (image_obj.image_rect.left - _offset/image_obj.depth, image_obj.image_rect.top))


    def render(self):
        self.screen.blit(self.bg_image, (0, 0))
        
    def update(self):
        self.frame_counter += globals.DELTA_TIME
    

    def stop(self):
        # del didn't do anything because python doesn't immediately GC anyways
        # use this method to stop music if there is any
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def ended(self) -> bool:
        pass
    
