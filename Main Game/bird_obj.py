import pygame
import sys
class bird_object:

    def __init__(self, path, x_size, y_size, x_pos, y_pos, depth, hp, regen_per_5_tic) -> None:
        self.image = pygame.image.load(path)  # Replace "your_image.png" with your image file path
        self.image_rect = self.image.get_rect()
        # Scale the image (change width and height as needed)
        self.scaled_width = x_size
        self.scaled_height = y_size
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))
        # Set the initial position of the image
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (x_pos, y_pos)
        self.depth = depth
        self.hp = hp
        self.max_hp = hp
        self.regen = regen_per_5_tic
        self.tic = 0
    
    def update(self):
        if self.hp + self.regen <= self.max_hp and self.tic >= 5:
            self.hp += self.regen
            self.tic = 0
        else:
            self.tic += 1