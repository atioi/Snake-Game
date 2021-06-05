import sys

import pygame
import pygame.transform

from game import Game
from menu import Menu

colors = {
    'board_color_1': (175, 215, 70),
    'board_color_2': (167, 209, 61),
    'snake_color': (48, 105, 152),
    'menu_color': (0, 0, 0)
}

fonts = {
    'menu': './fonts/LuckiestGuy-Regular.ttf'
}

class App:
    def __init__(self):
        # App dimensions
        self.__cell_number = 20
        self.__cell_size = 40

        # App state
        self.__state = 'menu'
        self.game = Game(self.__cell_size, self.__cell_number)

        #  Menu and submenus
        self.__menu = self.menu()
        self.__submenu = self.submenu()
        self.__pausemenu = self.pausemenu()

    def set_state(self, state: str):
        """
        This function sets app state.
        :param state: State name
        :return: None
        """
        self.__state = state

    def set_level(self, level):
        """
        This function sets game level
        :param level: game level (easy/medium/hard)
        :return: None
        """
        self.game.set_level(level)

    def menu(self):
        """
        This function creates a main menu.
        :return: Menu()
        """
        return Menu().build([
            ('play', lambda: self.play()),
            ('level', lambda: self.set_state('level')),
            ('exit', lambda: self.set_state('exit'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

    def submenu(self):
        """
        This function creates a submenu - the user interface to choose game level.
        :return: Menu()
        """
        return Menu().build([
            ('easy', lambda: self.game.set_level('easy')),
            ('medium', lambda: self.game.set_level('medium')),
            ('hard', lambda: self.game.set_level('hard'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

    def pausemenu(self):
        """
        This function creates a pause menu - the menu when user clicks ESCAPE button.
        :return: Menu()
        """
        return Menu().build([
            ('resume', lambda: self.set_state('game')),
            ('menu', lambda: self.set_state('menu')),
            ('exit', lambda: self.set_state('exit'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

    def play(self):
        self.game.reset()
        self.set_state('game')

    def lose(self):
        pass

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

            self.game.draw_background(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.__state == 'exit':
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    if self.__state == 'game':
                        self.game.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.__state == 'game':
                            self.set_state('pause')
                        elif self.__state == 'level':
                            self.set_state('menu')
                        elif self.__state == 'pause':
                            self.set_state('game')
                    else:
                        if self.__state == 'game':
                            self.game.key_event(event.key)
                        elif self.__state == 'menu':
                            self.__menu.key_event(event.key)
                        elif self.__state == 'level':
                            self.__submenu.key_event(event.key)
                        elif self.__state == 'pause':
                            self.__pausemenu.key_event(event.key)

            if self.__state == 'menu':
                self.__menu.display(screen)
            elif self.__state == 'game':
                self.game.draw(screen)
            elif self.__state == 'level':
                self.__submenu.display(screen)
            elif self.__state == 'pause':
                self.__pausemenu.display(screen)

            pygame.display.update()
            clock.tick(60)


App().window()
