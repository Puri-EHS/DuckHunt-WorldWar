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
    if (v[0] < 800 and v[0] > 0) and (v[1] < 425 and v[1] > 200): #limit the movement to the upper half of the screen
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
        return True #the reason this is to false is becuase this is the default    

class StrafingState(State):
    def __init__(self, probability_range) -> None:
        super().__init__()
        self.probabilty_range = probability_range
        self.prev_direction = 0
        
    def should_enter(self, ai):
        return distance(pygame.mouse.get_pos(), (ai.x, ai.y)) < 100
    
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
    
    
#assumption that no 2 states can be true at the same time
#go through every single state and the AI can enter
#when one of the states are true, then go into that state and call its execute function
class AI:
    def __init__(self):
        self.probability: int = random.randint(0, 100)
        self.states : list(State) = [StrafingState((0, 20)), FlyingState((0, 100))]
        self.current_state : State = None
        self.pick_new_point = None
        self.x = 500
        self.y = 400
        self.target_point = (-1, -1)
        self.velocity = 0.1
        self.slow = False
    def update_state(self):
        if(self.current_state is not None and self.current_state.exit_condition(self) is not True):
            return
        for state in self.states:
            if state.should_enter(self):
                self.current_state = state
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
        
        
        # Random stuff I added, probably should remove- AM
        if self.probability <= 2 and self.slow == False:
            self.velocity = 4
            self.slow = True
        if self.probability >= 95 and self.slow == True:
            self.velocity = 10
            self.slow = False

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set the size of the window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
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
    def on_shot(self, _damage):
        pass

    @abstractmethod
    def render(self, _screen, _camera_offset):
        pass

    @abstractmethod 
    def update(self):
        # AI.update() to figure out the position of the AI, and then set the rectangle of the enemy to that position
        pass