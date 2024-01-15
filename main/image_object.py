import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ImageObj:
    def __init__(self, path, depth, x_size, y_size, x_pos=SCREEN_WIDTH/2, y_pos=SCREEN_HEIGHT/2) -> None:
        self.image = pygame.image.load(path)  # Replace "your_image.png" with your image file path
        # Scale the image (change width and height as needed)
        self.image = pygame.transform.scale(self.image, (x_size, y_size))
        # Set the initial position of the image
        self.image_rect = self.image.get_rect()
        self.depth = depth
        self.x = x_pos
        self.y = y_pos
        self.image_rect.center = (x_pos, y_pos)
    
    def scale(self, factor):
        self.image = pygame.transform.scale(self.image, (self.image_rect.width * factor, self.image_rect.height * factor))
        #print(self.image_rect, self.image.get_rect())
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.x, self.y)
    
    def check_transparency(self, offset, x, y):
        
        x -= int(self.image_rect.left - offset/self.depth)
        y -= int(self.image_rect.top)

        print(self.image.get_at((x,y)).a)

        if self.image.get_at((x,y)).a == 0.0:
            return True
        else:
            return False
            