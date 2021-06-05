import random

import pygame
from pygame import *

from settings import *


class Fruit:
    def __init__(self, cell_size, cell_number):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.icon = pygame.image.load(image_paths['fruit'])

    def draw_fruit(self, surface):
        self.icon = pygame.transform.smoothscale(self.icon, (self.cell_size, self.cell_size))
        fruit_rect = pygame.Rect(int(self.pos.x * self.cell_size), int(self.pos.y * self.cell_size), self.cell_size,
                                 self.cell_size)
        surface.blit(self.icon, fruit_rect)
        # pygame.draw.rect(surface, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, self.cell_number - 1)
        self.y = random.randint(0, self.cell_number - 1)
        self.pos = Vector2(self.x, self.y)
