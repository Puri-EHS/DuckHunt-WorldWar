import random
import pygame
import math
import time
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
    

last_pop_time = time.time() #last time blud popped
pop_interval = 1.0  # Time in seconds between pops
is_duck_popped = False  # Track whether the duck is popped out or in cover

pick_new_point = True #should I pick a new point for flying
time_when_popped = 0
class dude2:
    def __init__(self, x, y, vel, duct_rect):
        self.x = x
        self.y = y
        self.velocity = vel
        self.possible_cover_points = [(330, 366), (422, 351), (379, 359), (490, 356), (670, 363), (600, 352), (31, 379), (141, 369), (241, 374), (744, 369), (658, 368)]
        #when the duck is strafing, it is moving side to side or up and down dodging shoots and shootin every so often
        #when the duck is taking cover it is rapidly flying downwards to duck from your fire
        #pop shooting is when the duck is behind cover and perodically popping its head up to shoot you 
        #flying is the default state where the duck is just casually flying in the air shooting you
        
        #strafing is activated when your crosshair is in proximity to the duck
        #pop shooting and Taking cover have a 80% chance to happen when you fire a shot at the duck and a 
        #40% chance to happen when your crosshair is close proximity to the duck
        self.states = ["STRAFING", "TAKING_COVER", "POP_SHOOTING", "FLYING"]
        self.state = "FLYING"
        self.lock_state = False
        self.duck_rect = duct_rect
        self.current_cover_point = None
        self.amount_of_pops = 0
        
        self.rand_point = (-1, -1)
        
        self.rand_cover_point = None
        
        #for strafting
        self.prev_direction = 0
        self.current_strafe_point = (-1, -1)

    def set_state(self):
        global time_when_popped
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
    
    
    #popping up and down behavior 
    def pop_behavior(self, pop_distance):
        global last_pop_time, is_duck_popped

        current_time = time.time()
        if current_time - last_pop_time > pop_interval:
            if(not is_duck_popped):
                self.rand_cover_point = self.get_random_cover_point()
            if is_duck_popped:
                # Duck back into cover
                self.duck_rect.topleft = self.rand_cover_point
            else:
                # Pop out of cover
                # Assuming the cover is vertical, and the duck pops up
                self.duck_rect.topleft = (self.rand_cover_point[0], self.rand_cover_point[1] - pop_distance)
                self.amount_of_pops += 1

            is_duck_popped = not is_duck_popped
            last_pop_time = current_time
    
    #taking cover logic
    def get_random_cover_point(self):
        return random.choice(self.possible_cover_points)
    
    def move_towards(self, target, speed):
        # Check if the duck has reached close enough to the target
        if abs(target[0] - self.duck_rect.x) <= speed and abs(target[1] - self.duck_rect.y) <= speed:
            self.duck_rect.topleft = target  # Snap to the exact target to prevent overshooting
            return True

        # Calculate the difference in x and y directions
        dx, dy = target[0] - self.duck_rect.x, target[1] - self.duck_rect.y
        distance = (dx**2 + dy**2)**0.5

        # Normalize the difference
        if distance == 0:  # Prevent division by zero
            return True  # The duck has reached the target

        nx, ny = dx / distance, dy / distance

        # Move the duck
        self.duck_rect.x += nx * speed
        self.duck_rect.y += ny * speed

        return False
    
    def pick_random_point(self):
        while(True):
            random_radius = random.randint(150, 250)
            rand_angle = random.uniform(-1 * math.pi/3, math.pi/3) +   (math.pi * random.randint(0, 1))
            
            self.rand_point = (self.x + (random_radius * math.cos(rand_angle)), self.y + (random_radius * math.sin(rand_angle)))
            if(in_bounds(self.rand_point)):
                break
            
               
        
    def flying(self):
        direction = subtract_vectors(self.rand_point, (self.duck_rect.x, self.duck_rect.y))
        distance = magnitude(direction)

        if distance < 5 or (self.rand_point[0] < 0 and self.rand_point[1] < 0):
            self.pick_random_point()
        else:
            normalized_direction = normalize(direction)
            self.duck_rect.x += normalized_direction[0] * self.velocity
            self.duck_rect.y += normalized_direction[1] * self.velocity
    
    
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
    
    def pick_random_strafe_point(self):
        #pick random angle
        #then pick random radius, so like polar coordinates
        while(True):
            angle = random.randrange(-30, 30)
            angle_in_radians = angle * 3.1415926535 / 180.0 + self.shift_angle()
            rand_radius = random.randrange(20, 30)
            self.current_strafe_point = (rand_radius * math.cos(angle_in_radians), rand_radius * math.sin(angle_in_radians))
            self.current_strafe_point = (self.current_strafe_point[0] + self.x, self.current_strafe_point[1] + self.y)
            if(in_bounds(self.current_strafe_point)):
                break
            
    def strafe_flying(self):
        direction = subtract_vectors(self.current_strafe_point, (self.duck_rect.x, self.duck_rect.y))
        distance = magnitude(direction)

        if distance < 5 or (self.current_strafe_point[0] < 0 and self.current_strafe_point[1] < 0):
            self.pick_random_strafe_point()
        else:
            normalized_direction = normalize(direction)
            self.duck_rect.x += normalized_direction[0] * self.velocity
            self.duck_rect.y += normalized_direction[1] * self.velocity
    
    
    def update(self):
        self.set_state()
        print(self.lock_state, self.state, self.duck_rect.topleft, self.duck_rect.x)
        if(self.state == self.states[0]):
            self.strafe_flying()
        elif(self.state == self.states[1]):
            self.move_towards((300, 300), 6)
        elif(self.state == self.states[2]):
            self.pop_behavior(120)
        else:
            self.flying()
            