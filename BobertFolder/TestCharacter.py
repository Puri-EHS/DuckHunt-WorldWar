import random
import pygame
import math
def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def magnitude(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    mag = magnitude(v)
    return (v[0]/mag, v[1]/mag)

def in_bounds(v):
    if (v[0] < 800 and v[0] > 0) and (v[1] < 300 and v[1] > 0): #limit the movement to the upper half of the screen
        return True
    return False
def quadratic_bezier_curve(p0, p1, p2, t):
    # Calculate the quadratic Bezier curve point at time t
    return (1-t)**2 * p0 + 2 * (1-t) * t * p1 + t**2 * p2

class dude:
    def __init__(self, x, y):
        self.prev_direction = 0
        self.fly_out_bezier = self.pick_random_flyout()
        self.t_val = 0
        self.in_flyout = True
        self.x = x
        self.y = y
        self.velocity = 0.1
        self.point_radius_min = 100 #in pixels
        self.point_radius_max = 200
        self.rand_point = (-5, -5)
        
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
            if(rando < 90):
                self.prev_direction = -1
                return 3.1415926535
            else:
                self.prev_direction = 1
                return 0
        if(self.prev_direction == -1):
            if(rando < 90):
                self.prev_direction = 1
                return 0
            else:
                self.prev_direction = -1
                return 3.1415926535

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)
    
    
    
    def pick_random_point(self):
        #pick random angle
        #then pick random radius, so like polar coordinates
        while(True):
            angle = random.randrange(-30, 30)
            angle_in_radians = angle * 3.1415926535 / 180.0 + self.shift_angle()
            rand_radius = random.randrange(self.point_radius_min, self.point_radius_max)
            self.rand_point = (rand_radius * math.cos(angle_in_radians), rand_radius * math.sin(angle_in_radians))
            self.rand_point = (self.rand_point[0] + self.x, self.rand_point[1] + self.y)
            if(in_bounds(self.rand_point)):
                break
        
        #shifting random point
    
    def pick_random_flyout(self):
        random_x = random.randrange(0, 800)
        p1 = (random_x, 300)
        p2 = (random.randrange(0, 800), random.randrange(0, 600))
        p3 = (random.randrange(0, 800), random.randrange(100, 200))
        return [p1, p2, p3]
    
    
    
    def update(self):
        direction = subtract_vectors(self.rand_point, (self.x, self.y))
        distance = magnitude(direction)

        # If close enough to the target, set a new random target
        if distance < 5 or (self.rand_point[0] < 0 and self.rand_point[1] < 0):
            self.pick_random_point()
        else:
            # Normalize the direction and move
            normalized_direction = normalize(direction)
            self.x += normalized_direction[0] * self.velocity
            self.y += normalized_direction[1] * self.velocity
