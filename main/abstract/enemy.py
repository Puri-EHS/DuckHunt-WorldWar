from abc import ABC, abstractmethod

import pygame

class Enemy(ABC):
    def __init__(self):
        self.depth = 0

        self.world_coordinates = (0, 0)
        self.screen_coordinates = (0, 0)

        self.health = 1

        self.sprite_sheet = None
        self.animation = None

        self.rect = None

    def get_screen_coordinates(self, _camera_offset):
        return (self.world_coordinates[0] - _camera_offset/self.depth, self.world_coordinates[1])

    def depth_render(self, _screen, _camera_offset):
        self.rect.center = self.get_screen_coordinates(_camera_offset)
        _screen.blit(self.animation.frames[self.animation.current_frame], self.rect.topleft)

    @abstractmethod
    def on_shot(self, _damage):
        pass

    def tryhit(self, _point, _damage):
        pass

    @abstractmethod
    def render(self, _screen, _camera_offset):
        pass

    @abstractmethod 
    def update(self):
        # use ai update then get state to update animation
        
        pass


class BasicAI:


    def __init__(self):
        pass

    
    
    

