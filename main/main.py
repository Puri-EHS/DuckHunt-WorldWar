import pygame

from game import Game
import constants

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

#initialize pygame 
pygame.display.set_caption("Fortnut Chapter 5")
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))


game = Game(screen)

game.switch_to_level(_level_index=game.current_level_index)

is_running = True
while is_running:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
            
        
    screen.fill((0, 0, 0))
    
    game.update()
    print(clock.get_fps())
    pygame.display.update()

    # game already runs at seconds per frame, so I disabled this for now
    # clock.tick(constants.FPS)
