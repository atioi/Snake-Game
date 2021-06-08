import os
import sys
import time

import pygame
import pygame.transform

from game import Game
from menu import Menu
from settings import *
from text import Text


class App:
    def __init__(self):
        # App dimensions
        self.__cell_number = 20
        self.__cell_size = 40
        self.best_result = (' ', 0, 0)

        # App state:
        self.__state = 'INTRO'
        self.game = Game(self, self.__cell_size, self.__cell_number)
        self.name = 'YOUR NAME'

        #  Menu and submenus:
        self.__menu = self.menu()
        self.__submenu = self.submenu()
        self.__pausemenu = self.pausemenu()
        self.__faultmenu = self.faultmenu()

        # Time
        self.start_time = 0
        self.time = 0
        self.flag = 0


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

    def read_file(self):
        """
        Read best result from file.
        :return: None
        """
        try:
            file = open(BEST_RESULTS_FILE_NAME, 'r')
            if os.stat(BEST_RESULTS_FILE_NAME).st_size != 0:
                self.best_result = tuple(file.readline().split())
            file.close()

        except FileNotFoundError:
            file = open(BEST_RESULTS_FILE_NAME, 'w')
            self.best_result = ('', 0, 0)
            file.close()

    def save_result(self):
        """
        Save result if is better than last one.
        :return: None
        """
        best_player_name, points, best_time = self.best_result
        if self.game.points > int(points):
            f = open("best.txt", "w")
            f.write(self.name + ' ' + str(self.game.points) + ' ' + str(self.game.end_time - self.start_time))
            f.close()



    def player_name(self, surface):
        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        if len(self.name) < 20:
            Text(self.name).color(COLORS['menu_color']).font(
                FONTS['menu']).font_size(60).position(
                (x, y_start + 2 * y_step)).render(
                surface)

    def intro(self, surface):
        self.read_file()

        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        Text('type your name').color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(20).position(
            (x, y_start + 3 * y_step)).render(
            surface)

    def fault(self, surface):

        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        # I use my own 'Text' class that is member of text.py file.

        Text('Your points: '). \
            color(COLORS['menu_color']). \
            font(FONTS['menu']). \
            font_size(50). \
            position((x, y_start)). \
            render(surface)

        Text(str(self.game.points)). \
            color(COLORS['menu_color']). \
            font(FONTS['menu']). \
            font_size(40). \
            position((x, y_start + y_step)). \
            render(surface)

        Text('Time:'). \
            color(COLORS['menu_color']). \
            font(FONTS['menu']). \
            font_size(50). \
            position((x, y_start + 2 * y_step)). \
            render(surface)

        self.time = self.game.end_time - self.start_time

        Text(str(self.time) + '  [s]'). \
            color(COLORS['menu_color']). \
            font(FONTS['menu']). \
            font_size(40).position((x, y_start + 3 * y_step)). \
            render(surface)

        self.__faultmenu.display(surface)
        self.save_result()

    def faultmenu(self):

        return Menu().build([
            ('restart', lambda: self.play()),
            ('menu', lambda: self.set_state('MENU')),
            ('exit', lambda: self.set_state('EXIT'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=450,
            y_step=70,
            color=COLORS['menu_color'],
            font_size=70,
            font=FONTS['menu'])

    def main_menu(self, surface):

        self.read_file()
        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        self.__menu.display(surface)

        Text('Best result').color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(50).position(
            (x, y_start + 5 * y_step)).render(surface)

        Text('name:').color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(40).position(
            (x, y_start + 6 * y_step)).render(surface)

        Text(str(self.best_result[0])).color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(25).position(
            (x, y_start + 6.5 * y_step)).render(surface)

        Text('points:').color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(40).position(
            (x, y_start + 7 * y_step)).render(surface)

        Text(str(self.best_result[1])).color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(25).position(
            (x, y_start + 7.5 * y_step)).render(surface)

        Text('time:').color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(40).position(
            (x, y_start + 8 * y_step)).render(surface)

        Text(str(self.best_result[2])).color(COLORS['menu_color']).font(
            FONTS['menu']).font_size(25).position(
            (x, y_start + 8.5 * y_step)).render(surface)

    def menu(self):
        """
        This function creates a main menu.
        :return: Menu()
        """

        return Menu().build([
            ('play', lambda: self.play()),
            ('level', lambda: self.set_state('LEVEL')),
            ('exit', lambda: self.set_state('EXIT'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=COLORS['menu_color'],
            font_size=70,
            font=FONTS['menu'])

    def set_level(self, level):
        self.set_state('MENU')
        self.game.set_level(level)

    def submenu(self):
        """
        This function creates a submenu - the user interface to choose game level.
        :return: Menu()
        """
        return Menu().build([
            ('easy', lambda: self.set_level('EASY')),
            ('medium', lambda: self.set_level('MEDIUM')),
            ('hard', lambda: self.set_level('HARD'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=COLORS['menu_color'],
            font_size=70,
            font=FONTS['menu'])

    def pausemenu(self):
        """
        This function creates a pause menu - the menu when user clicks ESCAPE button.
        :return: Menu()
        """
        return Menu().build([
            ('resume', lambda: self.set_state('GAME')),
            ('menu', lambda: self.set_state('MENU')),
            ('exit', lambda: self.set_state('EXIT'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=100,
            y_step=70,
            color=COLORS['menu_color'],
            font_size=70,
            font=FONTS['menu'])

    def play(self):
        self.time = 0
        self.game.points = 0
        self.start_time = time.time()
        self.game.reset()
        self.set_state('GAME')

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

        # App title and icon:
        snake_icon = pygame.image.load(ICONS_PATHS['snake'])
        pygame.display.set_icon(snake_icon)
        pygame.display.set_caption(APP_TITLE, APP_TITLE)

        while True:

            self.game.draw_background(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.__state == 'EXIT':
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    if self.__state == 'INTRO':
                        self.flag += 1
                        if self.flag == 7:
                            self.flag = 0
                    if self.__state == 'GAME':
                        self.game.update()

                if event.type == pygame.KEYDOWN:

                    if self.__state == 'INTRO':
                        key = event.key
                        if 48 <= key <= 57 or 65 <= key <= 90 or 97 <= key <= 122 and len(self.name) <= 10:
                            self.name += chr(key)
                        if key == pygame.K_BACKSPACE:
                            self.name = self.name[0:-1]
                        if key == pygame.K_RETURN and len(self.name) > 0:
                            self.set_state('MENU')
                    else:
                        if event.key == pygame.K_ESCAPE:
                            if self.__state == 'GAME':
                                self.save_result()
                                self.set_state('PAUSE')
                            elif self.__state == 'LEVEL':
                                self.set_state('MENU')
                            elif self.__state == 'PAUSE':
                                self.set_state('GAME')
                        else:
                            if self.__state == 'GAME':
                                self.game.key_event(event.key)
                            elif self.__state == 'MENU':
                                self.__menu.key_event(event.key)
                            elif self.__state == 'LEVEL':
                                self.__submenu.key_event(event.key)
                            elif self.__state == 'PAUSE':
                                self.__pausemenu.key_event(event.key)
                            elif self.__state == 'FAULT':
                                self.__faultmenu.key_event(event.key)

            if self.__state == 'MENU':
                self.main_menu(screen)
            elif self.__state == 'GAME':
                self.game.draw(screen)
            elif self.__state == 'LEVEL':
                self.__submenu.display(screen)
            elif self.__state == 'PAUSE':
                self.__pausemenu.display(screen)
            elif self.__state == 'FAULT':
                self.fault(screen)
            elif self.__state == 'INTRO':
                if self.flag < 5:
                    # To jest po to żeby nazwa gracza migła na samym początku gdy ma ją podać ..
                    self.player_name(screen)
                self.intro(screen)

            pygame.display.update()
            clock.tick(60)


App().window()
