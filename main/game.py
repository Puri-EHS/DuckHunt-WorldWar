from levels.splash_screen import SplashScreen
from levels.title_screen import TitleScreen
class Game:
    def __init__(self, _screen):
        self.current_level = None
        self.current_level_index = 0
        
        self.screen = _screen

        self.levels = [
            SplashScreen,
            TitleScreen
        ]

    def switch_to_level(self, _level_index):
        if(self.current_level is not None):
            self.current_level.stop()


        self.current_level_index = _level_index
        self.current_level = self.levels[_level_index]("level " + str(_level_index), self.screen, self)
        self.current_level.start()

    def update(self):
        # basic level switching
        # we can add transitions laterw
        if not self.current_level.ended():
            self.current_level.update()
        else:
            self.current_level_index += 1
            self.switch_to_level(self.current_level_index)
    

    @staticmethod
    def get_instance():
        return Game.instance