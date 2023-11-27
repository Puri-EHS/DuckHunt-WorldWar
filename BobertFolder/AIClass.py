import random
import pygame
import math
import time
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
class AI:
    def __init__(self, AI_rectangle : pygame.rect, strafing_probiility : float, ducking_speed : float, strafing_speed:float, flying_speed:float, flying_range : tuple, max_pop_amounts : int, flying_shooting_probability : float, popping_points : list):
        self.strafing_probility = strafing_probiility
        self.ducking_speed = ducking_speed
        self.strafing_speed = strafing_speed
        self.flying_speed = flying_speed
        self.flying_range = flying_range
        self.max_pop_amounts = max_pop_amounts
        self.flying_shooting_probility = flying_shooting_probability
        self.popping_points = popping_points
        self.AI_rectangle = AI_rectangle
        
        self.states = ["STRAFING", "TAKING_COVER", "POP_SHOOTING", "FLYING"]
        self.state = "FLYING"
        self.lock_state = False
        
        self.current_target_point = (-1, -1)
        self.current_cover_point = None
        self.amount_of_pops = 0
    
    def set_state(self):
        player_cursor_pos = pygame.mouse.get_pos()
        if(distance(player_cursor_pos, (self.duck_rect.x, self.duck_rect.y)) < 100 and not self.lock_state):
            if(random.randint(0, 100) < 60): #change back to 60
                self.lock_state = True
                self.state = self.states[0]
            else:
                self.lock_state = True
                self.state = self.states[1]
            return
        if(self.state == self.states[1] and self.move_towards((300, 300), 2)):
            self.lock_state = True
            self.state = self.states[2]
            return
        
        if(self.state == self.states[0] and distance(player_cursor_pos, (self.duck_rect.x, self.duck_rect.y)) > 200):
            self.lock_state = False
            self.state = self.states[3]
        if(self.amount_of_pops > 4):
            self.amount_of_pops = 0
            self.lock_state = False
            self.state = self.states[3]
        if(not self.lock_state and not self.state == self.states[1]):
            self.lock_state = False
            self.state = self.states[3] 

        
        
        
        
        
    