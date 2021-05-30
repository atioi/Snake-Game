import pygame.mouse


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.event = None

    def render(self):
        pass

    def add_event(self):
        x, y = pygame.mouse.get_pos()
