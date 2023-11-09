import pygame
import random
import math

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
class AICharacter:
    def __init__(self, position):
        self.position = position
        self.speed = 0.02  # Speed at which the AI moves along the curve

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.position.x), int(self.position.y)), 10)

def quadratic_bezier_curve(p0, p1, p2, t):
    # Calculate the quadratic Bezier curve point at time t
    return (1-t)**2 * p0 + 2 * (1-t) * t * p1 + t**2 * p2

control_points = [pygame.math.Vector2(random.randint(100, screen_width-100), random.randint(100, screen_height-100)) for _ in range(3)]
ai_character = AICharacter(control_points[0])
t = 0  # Parameter for the Bezier curve

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move along the Bezier curve
    t += ai_character.speed
    if t > 1:
        # Generate new control points and reset t
        control_points = [ai_character.position, pygame.math.Vector2(random.randint(100, screen_width-100), random.randint(100, screen_height-100)),  pygame.math.Vector2(random.randint(100, screen_width-100), random.randint(100, screen_height-100))]
        t = 0

    ai_character.position = quadratic_bezier_curve(control_points[0], control_points[1], control_points[2], t)

    screen.fill((0, 0, 0))
    ai_character.draw(screen)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()


