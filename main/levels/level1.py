from abstract.level import Level
from image_object import ImageObj
from enemies.vanila_duck import VanilaDuck
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from constants import SAVANNA_BUSH_FRONT, SAVANNA_BUSH_BACK, SAVANNA

class Level1(Level):
    def __init__(self, _name, _screen, _game_instance):
        super().__init__(_name, _screen, _game_instance)

        self.level_size = 1536

        self.background_image = [
            ImageObj(SAVANNA, 5, self.level_size, SCREEN_HEIGHT)
        ]
        
        self.images = [
            ImageObj(SAVANNA_BUSH_BACK, 4, 2100, 700, y_pos=500),
            ImageObj(SAVANNA_BUSH_FRONT, 3, 2000, 1000, y_pos=300)
        ]

        self.game_level = True

        self.alive_enemies = [
            VanilaDuck()
        ]
    
    def check_enemy_point_collisions(self, _point, _damage):
        for enemy in self.alive_enemies:
            if enemy.rect.collidepoint(_point):
                enemy.on_shot(_damage)
                if enemy.health <= 0:
                    self.alive_enemies.remove(enemy)
                    del enemy
                break


    def start(self):
        pass
    
    def render(self):
        # render background first
        self.depth_render(self.background_image, self.game_instance.player.x)

        # then enemies
        for enemy in self.alive_enemies:
            enemy.render(self.screen, self.game_instance.player.x)

        # then foreground images like bushes
        self.depth_render(self.images, self.game_instance.player.x)

    def update(self):
        for enemy in self.alive_enemies:
            enemy.update()

    
    def stop(self):
        del self

    def ended(self) -> bool:
        return False

    

    

    