import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ImageObj:
    def __init__(self, path, depth, x_size, y_size, x_pos=SCREEN_WIDTH/2, y_pos=SCREEN_HEIGHT/2) -> None:
        self.image = pygame.image.load(path)  # Replace "your_image.png" with your image file path
        # Scale the image (change width and height as needed)
        self.scaled_width = x_size
        self.scaled_height = y_size
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))
        # Set the initial position of the image
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (x_pos, y_pos)
        self.depth = depth
        self.x = x_pos
        self.y = y_pos

    