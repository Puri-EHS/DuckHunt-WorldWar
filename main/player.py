from constants import FPS
class Player:
    def __init__(self):
        self.x = 0
        self.gun = PlayerGun()

        self.max_ammo = 5
        self.ammo_left = self.max_ammo

        self.reload_time = 2.5 * FPS
        self.shoot_time = .5 * FPS

    def move(self, _x):
        self.x += _x
    
    def update(self):
        pass

    def shoot(self):
        pass

class PlayerGun:
    def __init__(self):
        pass