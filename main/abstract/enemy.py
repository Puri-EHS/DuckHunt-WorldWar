from abc import ABC, abstractmethod
import pygame
import random
import time
import math
import numpy
from player import Player
import globals
from globals import SCREEN_HEIGHT, SCREEN_WIDTH


def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def magnitude(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    mag = magnitude(v)
    return (v[0]/mag, v[1]/mag)

def in_bounds(v):
    if (v[1] < 425 and v[1] > 200): #limit the movement to the upper half of the screen
        return True
    return False

def distance(p1, p2):
    return math.sqrt(math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2))

def convert_global_x_coordinate(ai_x, player_x, depth):
    shifted_x = 0
    if(player_x / depth) >= 0:
        shifted_x = (ai_x - player_x / depth)
    else:
        shifted_x = (ai_x + math.fabs(player_x) / depth)
    return shifted_x


class State(ABC):
    def __init__(self, can_aim=True) -> None:
        self.can_aim = can_aim

    @abstractmethod
    def should_enter(self, ai):
        pass #when should it enter within this state, probability?
    
    @abstractmethod
    def execute(self, ai):
        pass #what should happen now that the AI is in this state
    
    @abstractmethod
    def exit_condition(self, ai):
        pass
    
class FlyingState(State):
    def __init__(self, probability_range, velocity) -> None:
        super().__init__()
        self.probabilty_range = probability_range
        self.velocity = velocity
        
    def should_enter(self, ai):
        return True #the reason for this is since this is the default state, so if no other states are valid, then this state always run
        #its important to put this as the last element in the AI states list, so it is the last state checked 
        
    def execute(self, ai):
        ai.velocity = self.velocity
        if(ai.pick_new_point):
            rand_y = random.randint(200, 425)
            rand_x = random.uniform(ai.player_reference.x / ai.depth, ai.player_reference.x / ai.depth + SCREEN_WIDTH)
            ai.target_point = (rand_x, rand_y)
    
    def exit_condition(self, ai):
        return True #the reason this is to True is becuase this is the default    
    

class StrafingState(State):
    def __init__(self, probability_range, velocity) -> None:
        super().__init__()
        self.velocity = velocity
        self.probability_range = probability_range
        self.prev_direction = 0
        
    def should_enter(self, ai):
        #coordinate shift moment
        shifted_x = convert_global_x_coordinate(ai.x, ai.player_reference.x, ai.depth)
        return distance(pygame.mouse.get_pos(), (shifted_x, ai.y)) < 200 and (ai.random_number < self.probability_range[1] and  ai.random_number > self.probability_range[0])
    
    def shift_angle(self):
        rando = random.randint(1, 100)
        if(self.prev_direction == 0):
            new_rando = random.randint(1, 2)
            if(new_rando == 1):
                self.prev_direction = -1
                return math.pi
            else:
                self.prev_direction = 0
                return 0
        if(self.prev_direction == 1):
            if(rando < 100):
                self.prev_direction = -1
                return math.pi
            else:
                self.prev_direction = 1
                return 0
        if(self.prev_direction == -1):
            if(rando < 100):
                self.prev_direction = 1
                return 0
            else:
                self.prev_direction = -1
                return math.pi

            
    def execute(self, ai):
        ai.velocity = self.velocity
        if(ai.pick_new_point):
            while(True):
                angle = random.randrange(-180, 180)
                angle_in_radians = angle * math.pi / 180.0 + self.shift_angle()
                rand_radius = random.randrange(60, 80)
                rand_point = (rand_radius * math.cos(angle_in_radians), rand_radius * math.sin(angle_in_radians))
                rand_point = (rand_point[0] + ai.x, rand_point[1] + ai.y)
                if(in_bounds(rand_point)):
                    ai.target_point = rand_point
                    break
    
    def exit_condition(self, ai):
        shifted_x = convert_global_x_coordinate(ai.x, ai.player_reference.x, ai.depth)
        return distance(pygame.mouse.get_pos(), (shifted_x, ai.y)) > 100

class DuckingState(State):
    def __init__(self, probability_range, velocity) -> None:
        super().__init__()
        self.velocity = velocity
        self.should_exit = False
        self.probability_range = probability_range
        self.last_pop_time = 0
        self.gotten_to_point = False
        self.is_duck_popped = False
        self.amount_of_pops = 0
    def should_enter(self, ai):
        return distance(pygame.mouse.get_pos(), (ai.x, ai.y)) < 100 and (ai.random_number < self.probability_range[1] and  ai.random_number > self.probability_range[0])
    
    def pop_behavior(self, ai, pop_distance, pop_interval):
        current_time = time.time()
        ai.velocity = 30
        if current_time - self.last_pop_time > pop_interval:
            if self.is_duck_popped:
                # Duck back into cover
                ai.target_point = (ai.target_point[0], ai.target_point[1] - pop_distance)
            else:
                # Pop out of cover
                # Assuming the cover is vertical, and the duck pops up
                ai.target_point = (ai.target_point[0], ai.target_point[1] + pop_distance)
                self.amount_of_pops += 1
            self.is_duck_popped = not self.is_duck_popped
            self.last_pop_time = current_time
    
    def execute(self, ai):
        ai.velocity = self.velocity
        # print(self.gotten_to_point)
        if(ai.pick_new_point and not self.gotten_to_point):
            ai.target_point = (300, 400)
            self.gotten_to_point = distance(ai.target_point, (ai.x, ai.y)) < 10
        if(self.gotten_to_point):
            self.pop_behavior(ai, 50, 1)
        
    def exit_condition(self, ai):
        if(self.amount_of_pops > 2):
            self.amount_of_pops = 0
            self.gotten_to_point = False
            return True
        return False
        

    
#assumption that no 2 states can be true at the same time
#go through every single state and the AI can enter
#when one of the states are true, then go into that state and call its execute function
class AI:
    def __init__(self, starting_x, starting_y, player_reference, depth, target_point = (-1, -1)):
        self.states : list(State) = [DuckingState((0, 0), 20), StrafingState((0, 100), 10), FlyingState((0, 100), 5)]
        self.current_state : State = None
        self.player_reference : Player = player_reference
        self.ducking = False
        self.depth = depth
        self.prev_state : State = None
        self.random_number = random.randint(0, 100)
        self.pick_new_point = True
        self.x = starting_x
        self.y = starting_y
        self.target_point = target_point
        self.velocity = 0
        self.normal_velocity = 0
        self.aiming_multiplier = 0.5
        self.shooting_multiplier = 0

    def update_state(self):
        if(self.current_state is not None and self.current_state.exit_condition(self) is not True):
            return
        self.random_number = random.randint(0, 100)
        for state in self.states:
            if state.should_enter(self):
                self.current_state = state
                if(self.current_state != self.prev_state):
                    self.pick_new_point = True
                self.prev_state = self.current_state
                break
        
    def move_to_point(self):
        direction = subtract_vectors(self.target_point, (self.x, self.y))
        distance = magnitude(direction)

        if distance < 5 or (self.target_point[0] < 0 and self.target_point[1] < 0):
            self.pick_new_point = True
        else:
            self.pick_new_point = False
            normalized_direction = normalize(direction)
            self.x += normalized_direction[0] * self.velocity * globals.DELTA_TIME
            self.y += normalized_direction[1] * self.velocity * globals.DELTA_TIME

    def update(self):
        shifted_x = convert_global_x_coordinate(self.x, self.player_reference.x, self.depth)
        print(self.current_state, distance(pygame.mouse.get_pos(), (shifted_x, self.y)))
        self.probability = random.randint(0, 100)
        self.update_state()
        self.current_state.execute(self)
        self.move_to_point()


class Enemy(ABC):
    def __init__(self):
        self.depth = 0
        self.player_ref = None

        self.world_coordinates = (0, 0)
        self.screen_coordinates = (0, 0)

        self.health = 1

        self.sprite_sheet = None
        self.animation = None

        self.rect = None



        #aim parameters
        self.x_change = 1
        self.y_change = 1
        self.p = .01 
        self.d = .1 
        self.xlasterror = 0
        self.ylasterror = 0
        self.random_multiplier = 4
        self.random_mean = 0
        self.random_std = 1.5
        self.aim_enter_prob = 1/200 #1/120
        self.aiming = False
        self.aim_coordinates = numpy.array([random.randrange(0, 1000), random.randrange(0, SCREEN_HEIGHT)])

        self.aim_line_x_offset = -46
        self.aim_line_y_offset = 0

        # Alex's way inferior code
        self.shoot_time = 4
        self.shoot_timer = 0
        self.firing = False

    def render_aim_line(self, _screen, _camera_offset):
        if self.aiming:
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 4)
        elif self.firing:
            pygame.draw.line(_screen, (255, 0, 0), (self.get_screen_coordinates(_camera_offset)[0] + self.aim_line_x_offset, self.get_screen_coordinates(_camera_offset)[1] + self.aim_line_y_offset), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 4)
            pygame.draw.circle(_screen, (255, 0, 0), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 200 - (self.shoot_timer*(200/self.shoot_time)), 4)


    def enter_aim(self):
        if not self.aiming and random.random() < self.aim_enter_prob and not self.firing:
            self.aiming = True
      
        #elif self.aiming and random.random() < self.aim_enter_prob:
            
     
    def aim(self):
        if self.aiming:

            xerror = self.player_ref.x - self.aim_coordinates[0]
            yerror = SCREEN_HEIGHT/2 - self.aim_coordinates[1]
            xerrorchange = xerror - self.xlasterror
            yerrorchange = yerror - self.ylasterror
            self.xlasterror = xerror
            self.ylasterror = yerror

             
            self.x_change += self.p * xerror + self.d * xerrorchange + self.random_multiplier * random.gauss(self.random_mean, self.random_std) * globals.DELTA_TIME
            self.y_change += self.p * yerror + self.d * yerrorchange + self.random_multiplier * random.gauss(self.random_mean, self.random_std) * globals.DELTA_TIME


            self.aim_coordinates[0] += self.x_change * globals.DELTA_TIME
            self.aim_coordinates[1] += self.y_change * globals.DELTA_TIME

            if random.random() < 1/100:
                self.aiming = False
                self.firing = True
        
        if self.firing:
            self.shoot_timer += globals.DELTA_TIME
            
            if self.shoot_timer >= self.shoot_time:
                self.firing = False
                self.shoot_timer = 0
                self.pop_a_cap(self.aim_coordinates)
            


    def pop_a_cap(self, coords):
        if self.player_ref.coords[0] - coords[0] > -200 and self.player_ref.coords[0] - coords[0] < 200:
            if self.player_ref.coords[1] - coords[1] > -150 and self.player_ref.coords[1] - coords[1] < 150:
                if not self.player_ref.ducking and not self.player_ref.gun.pause_no_con:
                    self.player_ref.hp -= 100


    def get_screen_coordinates(self, _camera_offset):
        return (self.world_coordinates[0] - _camera_offset/self.depth, self.world_coordinates[1]) 

    def depth_render(self, _screen, _camera_offset):
        self.rect.center = self.get_screen_coordinates(_camera_offset)
        _screen.blit(self.animation.frames[self.animation.current_frame], self.rect.topleft)

    @abstractmethod
    def on_shot(self, _damage):
        pass

    @abstractmethod
    def render(self, _screen, _camera_offset):
        pass

    @abstractmethod 
    def update(self):
        # AI.update() to figure out the position of the AI, and then set the rectangle of the enemy to that position
        pass