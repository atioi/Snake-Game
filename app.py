import sys

import pygame
import pygame.transform

from menu import Menu
from snake import Snake

colors = {
    'board_color_1': (175, 215, 70),
    'board_color_2': (167, 209, 61),
    'snake_color': (48, 105, 152),
    'menu_color': (0, 0, 0)
}


class App:
    def __init__(self):
        self.__cell_number = 20
        self.__cell_size = 40
        self.snake = Snake(self.__cell_size)
        self.level = 'easy'
        self.__state = 'menu'
        self.__menu = self.create_menu()
        self.__submenu = self.create_submenu()

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

    def set_state(self, state: str):
        """
        This function sets app state.
        :param state: State name
        :return: None
        """
        self.__state = state

    def set_level(self, level):
        self.level = 'easy'

    def create_menu(self):
        """
        This function creates menu using menu module.
        :return: menu.Menu()
        """
        menu = Menu()

        FONT = './fonts/LuckiestGuy-Regular.ttf'
        FONT_SIZE = 70
        COLOR = (0, 0, 0)

        menu.create_button('play', lambda: self.set_state('game'), COLOR, FONT_SIZE, FONT,
                           (self.__cell_size * self.__cell_number / 2, 70 + 5 * self.__cell_size))

        menu.create_button('level', lambda: self.set_state('level'), COLOR, FONT_SIZE, FONT,
                           (self.__cell_size * self.__cell_number / 2, 70 + 7 * self.__cell_size))

        return menu

    def create_submenu(self):
        """
        This function creates menu using menu module.
        :return: menu.Menu()
        """
        menu = Menu()

        FONT = './fonts/LuckiestGuy-Regular.ttf'
        FONT_SIZE = 70
        COLOR = (0, 0, 0)

        menu.create_button('easy', lambda: self.set_level('easy'), COLOR, FONT_SIZE, FONT,
                           (self.__cell_size * self.__cell_number / 2, 70 + 4 * self.__cell_size))

        menu.create_button('medium', lambda: self.set_level('medium'), COLOR, FONT_SIZE, FONT,
                           (self.__cell_size * self.__cell_number / 2, 70 + 6 * self.__cell_size))

        menu.create_button('hard', lambda: self.set_level('hard'), COLOR, FONT_SIZE, FONT,
                           (self.__cell_size * self.__cell_number / 2, 70 + 8 * self.__cell_size))

        return menu

    def game(self, surface):
        self.snake.draw_snake(surface)

    def window(self):
        """
        The main pygame - window loop.
        :return: None
        """
        pygame.init()

        screen_size = (self.__cell_number * self.__cell_size, self.__cell_number * self.__cell_size)
        screen = pygame.display.set_mode(screen_size)

        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, 150)
        clock = pygame.time.Clock()

        while True:

            self.draw_background(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    self.snake.move_snake()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.__state == 'menu':
                            self.__menu.click()
                    elif event.key == pygame.K_DOWN:
                        if self.__state == 'menu':
                            self.__menu.down()
                        elif self.__state == 'level':
                            self.__submenu.down()
                        elif self.__state == 'game':
                            self.snake.down()
                    elif event.key == pygame.K_UP:
                        if self.__state == 'menu':
                            self.__menu.up()
                        elif self.__state == 'level':
                            self.__submenu.up()
                        elif self.__state == 'game':
                            self.snake.up()
                    elif event.key == pygame.K_RIGHT:
                        if self.__state == 'game':
                            self.snake.right()
                    elif event.key == pygame.K_LEFT:
                        if self.__state == 'game':
                            self.snake.left()

            if self.__state == 'menu':
                self.__menu.display(screen)
            elif self.__state == 'game':
                self.game(screen)
            elif self.__state == 'level':
                self.__submenu.display(screen)

            pygame.display.update()
            clock.tick(60)


App().window()
