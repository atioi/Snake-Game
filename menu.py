from pygamex import *


class Menu:
    def __init__(self):
        self.__menu = []
        self.__pointer = 0

    def create_button(self, name, function, color=(0, 0, 0), size=25, font=None, position=(0, 0)):
        """
        This function "creates" menu's button using Text class from pygamex.
        :param position:
        :param font:
        :param size:
        :param color:
        :param name: button name eg. 'start'
        :param function: Function that will be execute when button is clicked.
        :return:
        """

        button_surface = Text(name, color, size, font, position)
        self.__menu.append((name, button_surface, function))

    def display(self, surface):
        """
        This function displays menu on a screen.
        :param surface: pygame.surface
        :return: None
        """

        self.on_hover()

        for index, opt in enumerate(self.__menu):
            name, value, function = opt
            value.render(surface)

    def up(self):
        self.off_hover()
        self.__pointer -= 1

    def down(self):
        self.off_hover()
        self.__pointer += 1

    def off_hover(self):
        name, value, function = self.__menu[self.__pointer % len(self.__menu)]
        value.color((0, 0, 0))

    def on_hover(self):
        name, value, function = self.__menu[self.__pointer % len(self.__menu)]
        value.color((48, 105, 152))

    def click(self):
        """
        This function runs option's function that self.__pointer points at.
        :return: None
        """
        name, value, function = self.__menu[self.__pointer % len(self.__menu)]
        function()
