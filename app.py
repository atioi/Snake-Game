import sys
import time

import pygame
import pygame.transform

from game import Game
from menu import Menu
from settings import icons_paths
from text import Text

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
        self.best_result = ('', 0, 0)
        # App state
        self.__state = 'INTRO'
        self.game = Game(self, self.__cell_size, self.__cell_number)
        self.name = 'player'
        #  Menu and submenus
        self.__menu = self.menu()
        self.__submenu = self.submenu()
        self.__pausemenu = self.pausemenu()
        self.__faultmenu = self.faultmenu()
        self.start_time = True
        self.time = 0
        self.flag = 0

    def save_result(self):
        name, points, time = self.best_result
        print(points)
        if self.game.points > int(points):
            f = open("dw23c.txt", "w")
            f.write(self.name + ' ' + str(self.game.points) + ' ' + str(self.game.end_time - self.start_time))
            f.close()

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

    def player_name(self, surface):
        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        if len(self.name) < 20:
            Text(self.name).color(colors['menu_color']).font(
                fonts['menu']).font_size(60).position(
                (x, y_start + 2 * y_step)).render(
                surface)

    def read(self):
        try:
            f = open("dw23c.txt", 'r')
            self.best_result = f.read()
            self.best_result = self.best_result.split()
            self.best_result = (self.best_result[0], self.best_result[1], self.best_result[2])
            f.close()
        except:
            f = open("dw23c.txt", 'w')
            f.close()

    def intro(self, surface):
        self.read()

        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        Text('type your name').color(colors['menu_color']).font(
            fonts['menu']).font_size(20).position(
            (x, y_start + 3 * y_step)).render(
            surface)

    def fault(self, surface):
        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70
        Text('Your points: ').color(colors['menu_color']).font(fonts['menu']).font_size(50).position(
            (x, y_start)).render(surface)

        Text(str(self.game.points)).color(colors['menu_color']).font(
            fonts['menu']).font_size(40).position(
            (x, y_start + y_step)).render(
            surface)

        Text('Time:').color(colors['menu_color']).font(
            fonts['menu']).font_size(50).position(
            (x, y_start + 2 * y_step)).render(surface)

        self.time = self.game.end_time - self.start_time
        Text(str(self.time) + '  [s]').color(colors['menu_color']).font(
            fonts['menu']).font_size(40).position(
            (x, y_start + 3 * y_step)).render(surface)

        self.__faultmenu.display(surface)

    def faultmenu(self):
        return Menu().build([
            ('restart', lambda: self.play()),
            ('menu', lambda: self.set_state('MENU')),
            ('exit', lambda: self.set_state('EXIT'))
        ],
            x=self.__cell_size * self.__cell_number / 2,
            y_start=450,
            y_step=70,
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

    def main_menu(self, surface):
        self.read()
        x = self.__cell_size * self.__cell_number / 2
        y_start = 100
        y_step = 70

        self.__menu.display(surface)

        Text('Best result').color(colors['menu_color']).font(
            fonts['menu']).font_size(50).position(
            (x, y_start + 4.2 * y_step)).render(surface)

        Text('name:').color(colors['menu_color']).font(
            fonts['menu']).font_size(40).position(
            (x, y_start + 5 * y_step)).render(surface)

        Text(str(self.best_result[0])).color(colors['menu_color']).font(
            fonts['menu']).font_size(25).position(
            (x, y_start + 5.6 * y_step)).render(surface)

        Text('points:').color(colors['menu_color']).font(
            fonts['menu']).font_size(40).position(
            (x, y_start + 6 * y_step)).render(surface)

        Text(str(self.best_result[1])).color(colors['menu_color']).font(
            fonts['menu']).font_size(25).position(
            (x, y_start + 6.6 * y_step)).render(surface)

        Text('time:').color(colors['menu_color']).font(
            fonts['menu']).font_size(40).position(
            (x, y_start + 7 * y_step)).render(surface)

        Text(str(self.best_result[2])).color(colors['menu_color']).font(
            fonts['menu']).font_size(25).position(
            (x, y_start + 7.6 * y_step)).render(surface)

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
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

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
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

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
            color=colors['menu_color'],
            font_size=70,
            font=fonts['menu'])

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

        while True:

            self.game.draw_background(screen)
            icon = pygame.image.load(icons_paths['snake'])
            pygame.display.set_icon(icon)
            pygame.display.set_caption('Snake', 'Snake')
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
                        if key == pygame.K_RETURN:
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
                    self.player_name(screen)
                self.intro(screen)

            pygame.display.update()
            clock.tick(60)


App().window()
