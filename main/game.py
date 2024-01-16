from levels.splash_screen import SplashScreen
from levels.title_screen import TitleScreen
from levels.target_practice import TargetPractice
from levels.Controller_img import Cont_img
from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3
from levels.Loading_screen import LoadingScreen
from levels.lev1_victory import lev1_victory
from levels.lev2_victory import lev2_victory
from levels.lev3_victory import lev3_victory
from levels.ded import Ded
from levels.options_screen import OptionScreen
from constants import USE_MOUSE
from player import Player

import pygame

class Game:
    def __init__(self, _screen):
        self.current_level = None
        self.current_level_index = 0 #should be set to zero usually, 1 will skip the splash screen
        self.lev_ded_on = 0
        self.screen = _screen

        self.player = Player(self)

        self.ded_screen = Ded

        if USE_MOUSE:
            self.levels = [
                SplashScreen,
                TitleScreen,
                OptionScreen,
                ##TargetPractice
                LoadingScreen,
                Level1,
                lev1_victory,
                LoadingScreen,
                Level2,
                lev2_victory,
                LoadingScreen,
                Level3,
                lev3_victory,
                LoadingScreen,
                Ded
            ]

        else:
            self.levels = [
                SplashScreen,
                TitleScreen,
                OptionScreen,
                Cont_img,
                ##TargetPractice
                LoadingScreen,
                Level1,
                lev1_victory,
                LoadingScreen,
                Level2,
                lev2_victory,
                LoadingScreen,
                Level3,
                lev3_victory,
                LoadingScreen,
                Ded
            ]

    def switch_to_level(self, _level_index):
        if(self.current_level is not None):
            self.current_level.stop()
        print(_level_index)
        self.current_level_index = _level_index
        self.current_level = self.levels[_level_index]("level " + str(_level_index), self.screen, self)
        self.current_level.start()

    def update(self):

        if self.player.hp <= 0:
            self.player.hp = 100
            self.lev_ded_on = self.current_level_index
            self.current_level_index = 12
            self.switch_to_level(self.current_level_index)
        
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
        
        elif self.current_level_index == 12:
            self.current_level_index = self.lev_ded_on - 1
            self.switch_to_level(self.current_level_index)
        
        elif self.current_level_index == 11:
            self.lev_ded_on = 0
            self.current_level_index = 1
            self.switch_to_level(self.current_level_index)

        else:
            self.current_level_index += 1
            self.switch_to_level(self.current_level_index)

    


    