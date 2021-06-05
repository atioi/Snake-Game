import pygame

from fruit import Fruit
from snake import Snake

colors = {
    'board_color_1': (175, 215, 70),
    'board_color_2': (167, 209, 61),
    'snake_color': (48, 105, 152),
    'menu_color': (0, 0, 0)
}


class Game:
    def __init__(self, cell_size, cell_number, level='easy'):
        self.__level = level
        self.__cell_size = cell_size
        self.__cell_number = cell_number
        self.__snake = Snake(self.__cell_size)
        self.__fruit = Fruit(self.__cell_size, self.__cell_number)
        self.points = 0

    def draw(self, surface):
        self.__fruit.draw_fruit(surface)
        self.__snake.draw_snake(surface)

    def draw_background(self, surface):
        surface.fill(colors['board_color_1'])
        for row in range(self.__cell_number):
            if row % 2 == 0:
                for col in range(self.__cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.__cell_size, row * self.__cell_size, self.__cell_size,
                                                 self.__cell_size)
                        pygame.draw.rect(surface, colors['board_color_2'], grass_rect)
            else:
                for col in range(self.__cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.__cell_size, row * self.__cell_size, self.__cell_size,
                                                 self.__cell_size)
                        pygame.draw.rect(surface, colors['board_color_2'], grass_rect)

    def set_level(self, level):
        self.__level = level

    def up(self):
        self.__snake.up()

    def down(self):
        self.__snake.down()

    def right(self):
        self.__snake.right()

    def left(self):
        self.__snake.left()

    def easy(self):
        if self.__snake.body[0].x < 0:
            self.__snake.body[0].x = self.__cell_number
        elif self.__snake.body[0].x > self.__cell_number:
            self.__snake.body[0].x = 0
        elif self.__snake.body[0].y < 0:
            self.__snake.body[0].y = self.__cell_number
        elif self.__snake.body[0].y > self.__cell_number:
            self.__snake.body[0].y = 0

    def medium(self):
        if self.__snake.body[0].x < 0:
            print('FAULT')
        elif self.__snake.body[0].x > self.__cell_number:
            print('FAULT')
        elif self.__snake.body[0].y < 0:
            print('FAULT')
        elif self.__snake.body[0].y > self.__cell_number:
            print('FAULT')

    def hard(self):
        pass

    def update(self):
        self.__snake.move_snake()
        self.check_fruit_col()

        if self.__level == 'easy':
            self.easy()
        elif self.__level == 'medium':
            self.medium()
        elif self.__level == 'hard':
            self.hard()

    def reset(self):
        self.__snake.reset()
        self.points = 0

    def check_fruit_col(self):
        if self.__snake.body[0] == self.__fruit.pos:
            self.__fruit.randomize()
            self.__snake.new_block = True

    def key_event(self, key):
        if key == pygame.K_UP:
            self.up()
        elif key == pygame.K_DOWN:
            self.down()
        elif key == pygame.K_LEFT:
            self.left()
        elif key == pygame.K_RIGHT:
            self.right()
