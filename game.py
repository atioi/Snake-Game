import time

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
    def __init__(self, app, cell_size, cell_number, level='EASY'):
        self.__level = level
        self.app = app
        self.__cell_size = cell_size
        self.__cell_number = cell_number
        self.__snake = Snake(self.__cell_size)
        self.__fruit = Fruit(self.__cell_size, self.__cell_number)
        self.points = 0
        self.end_time = 0

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
        if self.__snake.body[0].y < 0 or self.__snake.body[2].y < 0:
            self.app.set_state('FAULT')
            self.end_time = time.time()
            self.app.save_result()

        elif self.__snake.body[0].y >= self.__cell_number or self.__snake.body[2].y >= self.__cell_number:
            self.app.set_state('FAULT')
            self.end_time = time.time()
            self.app.save_result()

        elif self.__snake.body[0].x < 0 or self.__snake.body[2].x < 0:
            self.app.set_state('FAULT')
            self.end_time = time.time()
            self.app.save_result()


        elif self.__snake.body[0].x >= self.__cell_number or self.__snake.body[2].x >= self.__cell_number:
            self.app.set_state('FAULT')
            self.end_time = time.time()
            self.app.save_result()

    def hard(self):
        self.medium()

    def update(self):
        self.check_yourself_col()
        self.__snake.move_snake()
        self.check_fruit_col()

        if self.__level == 'EASY':
            pygame.time.set_timer(pygame.USEREVENT, 150)
            self.easy()
        elif self.__level == 'MEDIUM':
            pygame.time.set_timer(pygame.USEREVENT, 150)
            self.medium()
        elif self.__level == 'HARD':
            pygame.time.set_timer(pygame.USEREVENT, 50)
            self.hard()

    def reset(self):
        self.__fruit.randomize()
        self.__snake.reset()
        self.points = 0

    def check_fruit_col(self):
        if self.__snake.body[0] == self.__fruit.pos:
            self.__fruit.randomize()
            self.__snake.new_block = True
            self.points += 1

    def check_yourself_col(self):
        head = self.__snake.body[0]
        for index, part in enumerate(self.__snake.body):
            if index > 0 and head.x == part.x and head.y == part.y:
                self.app.set_state('FAULT')
                self.app.save_result()
                self.end_time = time.time()
                self.app.time = self.end_time - self.app.start_time

    def key_event(self, key):
        if self.__snake.steer == True:
            if key == pygame.K_UP:
                if self.__snake.direction.y != 1:
                    self.__snake.steer = False
                    self.up()
            if key == pygame.K_DOWN:
                if self.__snake.direction.y != -1:
                    self.__snake.steer = False
                    self.down()
            if key == pygame.K_LEFT:
                if self.__snake.direction.x != 1:
                    self.__snake.steer = False
                    self.left()
            if key == pygame.K_RIGHT:
                if self.__snake.direction.x != -1:
                    self.__snake.steer = False
                    self.right()
