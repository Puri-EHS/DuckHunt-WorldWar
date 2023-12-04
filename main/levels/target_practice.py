from abstract.level import Level
from image_object import ImageObj
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from constants import SAVANNA_BUSH_FRONT, SAVANNA_BUSH_BACK, SAVANNA

class TargetPractice(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)

        self.level_size = 1536

        self.background_image = [
            ImageObj(SAVANNA, 5, self.level_size, SCREEN_HEIGHT)
        ]
        
        self.images = [
            ImageObj(SAVANNA_BUSH_BACK, 4, 2100, 700, 400),
            ImageObj(SAVANNA_BUSH_FRONT, 3, 2000, 1000, 250)
        ]

        self.game_level = True


    
    def start(self):
        pass
    
    def render(self):
        # render background first
        self.depth_render(self.background_image, self.game_instance.player.x)

        # then enemies

        # then foreground images like bushes
        self.depth_render(self.images, self.game_instance.player.x)

    def update(self):
        pass
        # self.render()
    
    def stop(self):
        del self

    def ended(self) -> bool:
        return False

    

    

    