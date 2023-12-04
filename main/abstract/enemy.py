from abc import ABC, abstractmethod


class Enemy(ABC):
    def __init__(self):
        self.depth = 0

        self.world_coordinates = (0, 0)
        self.screen_coordinates = (0, 0)

        self.health = 1
        
    @abstractmethod 
    def update(self):
        # use ai update then get state to update animation
        
        pass


class BasicAI:
    def __init__(self):
        pass

    
    
    

