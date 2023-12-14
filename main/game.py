from levels.splash_screen import SplashScreen
from levels.title_screen import TitleScreen
from levels.target_practice import TargetPractice
from levels.Controller_img import Cont_img
from constants import USE_MOUSE
from player import Player

import pygame

class Game:
    def __init__(self, _screen):
        self.current_level = None
        self.current_level_index = 2 #should be set to zero usually, 1 will skip the splash screen
        
        self.screen = _screen

        self.player = Player(self)

        if USE_MOUSE:
            self.levels = [
                SplashScreen,
                TitleScreen,
                TargetPractice
            ]
        else:
            self.levels = [
                SplashScreen,
                TitleScreen,
                Cont_img,
                TargetPractice
            ]

    def switch_to_level(self, _level_index):
        if(self.current_level is not None):
            self.current_level.stop()

        self.current_level_index = _level_index
        self.current_level = self.levels[_level_index]("level " + str(_level_index), self.screen, self)
        self.current_level.start()

    def update(self):

        #player input
        if self.current_level.game_level:
            self.player.handle_input(self.current_level.level_size)

            self.player.gun.update()
            self.player.update()


        # basic level switching
        # we can add transitions later
        if not self.current_level.ended():
            self.current_level.update()
            self.current_level.render()
            if self.current_level.game_level:
                self.player.gun.render(self.screen)
        else:
            self.current_level_index += 1
            self.switch_to_level(self.current_level_index)

    


    