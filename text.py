import pygame

class Text:
    def __init__(self, text, color=(0, 0, 0), size=25, font=None, position=(0, 0)):
        self.__text = text
        self.__font = font
        self.__color = color
        self.__size = size

        self.__surface = None
        self.__antialias = False
        self.__pygame_font = None
        self.__position = position

    def render(self, surface):
        x, y = self.__position
        self.__pygame_font = pygame.font.Font(self.__font, self.__size)
        text_surface = self.__pygame_font.render(self.__text, self.__antialias, self.__color)
        width = text_surface.get_width()
        surface.blit(text_surface, (x - width / 2, y))

    def color(self, color):
        self.__color = color
        return self

    def font(self, font):
        self.__font = font
        return self

    def font_size(self, size):
        self.__size = size
        return self

    def position(self, position):
        self.__position = position
        return self
