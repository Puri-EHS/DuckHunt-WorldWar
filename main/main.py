import pygame

from game import Game
from player_gun import PlayerGun
from levels.splash_screen import SplashScreen
import constants

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

#initialize pygame 
pygame.display.set_caption("Fortnut Chapter 5")
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))


game = Game(screen)

game.switch_to_level(_level_index = 0)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
        
    screen.fill((0, 0, 0))
    
    game.update()
    
    pygame.display.update()

    clock.tick(constants.FPS)
