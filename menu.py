from pygamex import *


class Menu:
    def __init__(self):
        self.__menu = []
        self.__pointer = 0

    def create_button(self, name, function, color=(0, 0, 0), size=25, font=None, position=(0, 0)):
        button_surface = Text(name, color, size, font, position)
        self.__menu.append((name, button_surface, function))

    def display(self, surface):
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

    def build(self, buttons, x, y_start, y_step, color, font_size, font):
        """
        This function build automatically menu from given:
        :param buttons: array[(str, function),..] - array of tuples that contains button's text and button's function
        :param x: menu x position
        :param y_start: menu y start position
        :param y_step: Space between buttons
        :param color: menu's buttons' color
        :param font_size: menu's buttons' font size
        :param font: menu's buttons' font
        :return: Menu()
        """
        for index, value in enumerate(buttons):
            text, function = value
            self.create_button(text, function, color, font_size, font,
                               (x, y_start + index * y_step))
        return self

    def key_event(self, key):
        if key == pygame.K_UP:
            self.up()
        elif key == pygame.K_DOWN:
            self.down()
        elif key == pygame.K_RETURN:
            self.click()

