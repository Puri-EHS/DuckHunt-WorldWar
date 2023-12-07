from abc import ABC, abstractmethod
import pygame
import random
import time
import math
import numpy

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def magnitude(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    mag = magnitude(v)
    return (v[0]/mag, v[1]/mag)

def in_bounds(v):
    if (v[0] < 800 and v[0] > 0) and (v[1] < 250 and v[1] > 0): #limit the movement to the upper half of the screen
        return True
    return False

def distance(p1, p2):
    return math.sqrt(math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2))


class State(ABC):
    @abstractmethod
    def should_enter(self, ai):
        pass #when should it enter within this state, probability?
    
    @abstractmethod
    def execute(self, ai):
        pass #what should happen now that the AI is in this state
    
    
class FlyingState(State):
    def __init__(self, probability_range) -> None:
        super().__init__()
        self.probabilty_range = probability_range
        
    def should_enter(self, ai):
        return ai.probability < self.probabilty_range[1] and ai.probability > self.probabilty_range[0]
    
    def execute(self, ai):
        if(ai.pick_new_point):
            while(True):
                random_radius = random.randint(150, 300)
                rand_angle = random.randint(0, 360) * math.pi/ 180
                rand_point = (ai.x + (random_radius * math.cos(rand_angle)), ai.y + (random_radius * math.sin(rand_angle)))
                if(in_bounds(rand_point)):
                    ai.target_point = rand_point
                    break
    

class StrafingState(State):
    def __init__(self, probability_range) -> None:
        super().__init__()
        self.probabilty_range = probability_range
        
    def should_enter(self, ai):
        return ai.probability < self.probabilty_range[1] and ai.probability > self.probabilty_range[0]
    
    def shift_angle(self):
        rando = random.randint(1, 100)
        if(self.prev_direction == 0):
            new_rando = random.randint(1, 2)
            if(new_rando == 1):
                self.prev_direction = -1
                return 3.1416926535
            else:
                self.prev_direction = 0
                return 0
        if(self.prev_direction == 1):
            if(rando < 100):
                self.prev_direction = -1
                return 3.1415926535
            else:
                self.prev_direction = 1
                return 0
        if(self.prev_direction == -1):
            if(rando < 100):
                self.prev_direction = 1
                return 0
            else:
                self.prev_direction = -1
                return 3.1415926535
            
    def execute(self, ai):
        #pick random angle
        #then pick random radius, so like polar coordinates
        if(ai.pick_new_point):
            while(True):
                angle = random.randrange(-30, 30)
                angle_in_radians = angle * 3.1415926535 / 180.0 + self.shift_angle()
                rand_radius = random.randrange(50, 80)
                rand_point = (rand_radius * math.cos(angle_in_radians), rand_radius * math.sin(angle_in_radians))
                rand_point = (rand_point[0] + ai.x, rand_point[1] + ai.y)
                if(in_bounds(rand_point)):
                    ai.target_point = rand_point
                    break
    
    
#assumption that no 2 states can be true at the same time
#go through every single state and the AI can enter
#when one of the states are true, then go into that state and call its execute function
class AI:
    def __init__(self):
        self.probability: int = random.randint(0, 100)
        self.states : list(State) = [StrafingState((0, 20)), FlyingState((0, 100))]
        self.current_state : State = None
        self.pick_new_point = True
        self.x = 500
        self.y = 300
        self.target_point = (-1, -1)
    def update_state(self):
        for state in self.states:
            if state.should_enter(self):
                self.current_state = state
                break
    
    def update(self):
        self.probability = random.randint(0, 100)
        self.update_state()
        self.current_state.execute(self)
        
        

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
    def render(self, _screen, _camera_offset):
        pass

    @abstractmethod 
    def update(self):
        # AI.update() to figure out the position of the AI, and then set the rectangle of the enemy to that position
        pass