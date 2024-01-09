from abc import ABC, abstractmethod
import pygame
import random
import time
import math
import numpy
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def magnitude(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    mag = magnitude(v)
    return (v[0]/mag, v[1]/mag)

def in_bounds(v):
    if (v[0] < 800 and v[0] > 0) and (v[1] < 425 and v[1] > 200): #limit the movement to the upper half of the screen
        return True
    return False

def distance(p1, p2):
    return math.sqrt(math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2))


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
    def __init__(self, probability_range) -> None:
        super().__init__()
        self.probabilty_range = probability_range
        
    def should_enter(self, ai):
        return True #the reason for this is since this is the default state, so if no other states are valid, then this state always run
        #its important to put this as the last element in the AI states list, so it is the last state checked 
        
    def execute(self, ai):
        if(ai.pick_new_point):
            while(True):
                random_radius = random.randint(150, 300)
                rand_angle = random.randint(0, 360) * math.pi/ 180
                rand_point = (ai.x + (random_radius * math.cos(rand_angle)), ai.y + (random_radius * math.sin(rand_angle)))
                if(in_bounds(rand_point)):
                    ai.target_point = rand_point
                    break
    def exit_condition(self, ai):
        return True #the reason this is to True is becuase this is the default    
    

class StrafingState(State):
    def __init__(self, probability_range) -> None:
        super().__init__()
        self.probability_range = probability_range
        self.prev_direction = 0
        
    def should_enter(self, ai):
        return distance(pygame.mouse.get_pos(), (ai.x, ai.y)) < 100 and (ai.random_number < self.probability_range[1] and  ai.random_number > self.probability_range[0])
    
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
        ai.velocity = 5
        if(ai.pick_new_point):
            while(True):
                angle = random.randrange(-70, 70)
                angle_in_radians = angle * 3.1415926535 / 180.0 + self.shift_angle()
                rand_radius = random.randrange(60, 80)
                rand_point = (rand_radius * math.cos(angle_in_radians), rand_radius * math.sin(angle_in_radians))
                rand_point = (rand_point[0] + ai.x, rand_point[1] + ai.y)
                if(in_bounds(rand_point)):
                    ai.target_point = rand_point
                    break
    def exit_condition(self, ai):
        return distance(pygame.mouse.get_pos(), (ai.x, ai.y)) > 100

class DuckingState(State):
    def __init__(self, probability_range) -> None:
        super().__init__()
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
        ai.velocity = 10
        if current_time - self.last_pop_time > pop_interval:
            if self.is_duck_popped:
                # Duck back into cover
                # print("back down")
                ai.target_point = (ai.target_point[0], ai.target_point[1] - pop_distance)
            else:
                # Pop out of cover
                # print("going up")
                # Assuming the cover is vertical, and the duck pops up
                ai.target_point = (ai.target_point[0], ai.target_point[1] + pop_distance)
                self.amount_of_pops += 1
            self.is_duck_popped = not self.is_duck_popped
            self.last_pop_time = current_time
    
    def execute(self, ai):
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
    def __init__(self):
        self.probability: int = random.randint(0, 100)
        self.states : list(State) = [DuckingState((0, 100)), StrafingState((0, 0)), FlyingState((0, 100))]
        self.current_state : State = None
        self.prev_state : State = None
        self.random_number = random.randint(0, 100)
        self.pick_new_point = None
        self.x = 500
        self.y = 400
        self.target_point = (-1, -1)
        self.velocity = 0.1
        self.slow = False
    
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
            self.x += normalized_direction[0] * self.velocity
            self.y += normalized_direction[1] * self.velocity
    
    def update(self):
        self.probability = random.randint(0, 100)
        self.update_state()
        self.current_state.execute(self)
        self.move_to_point()
        #print(self.target_point)
        
        

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set the size of the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rectangle Display")

    # Define rectangle parameters
    rect_width = 50
    rect_height = 50
    rect_color = (255, 0, 0)  # Red color

    # Main loop
    running = True
    AI_test = AI()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color (optional)
        screen.fill((0, 0, 0))  # Black color

        # Draw the rectangle
        AI_test.update()
        pygame.draw.rect(screen, rect_color, (AI_test.x, AI_test.y, rect_width, rect_height))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()        

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
        self.aim_enter_prob = 1/240 #1/120
        self.aiming = False
        self.aim_coordinates = numpy.array([random.randrange(0, 1000), random.randrange(0, SCREEN_HEIGHT)])



    def render_aim_line(self, _screen, _camera_offset):
        if self.aiming:
            pygame.draw.line(_screen, (255, 0, 0), self.get_screen_coordinates(_camera_offset), (self.aim_coordinates[0] - self.player_ref.x + SCREEN_WIDTH/2, self.aim_coordinates[1]), 4)

    def enter_aim(self):
        if not self.aiming and random.random() < self.aim_enter_prob:
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

             
            self.x_change += self.p * xerror + self.d * xerrorchange + self.random_multiplier * random.gauss(self.random_mean, self.random_std)
            self.y_change += self.p * yerror + self.d * yerrorchange + self.random_multiplier * random.gauss(self.random_mean, self.random_std)

            # normal distribution random



            self.aim_coordinates[0] += self.x_change
            self.aim_coordinates[1] += self.y_change
            

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