import sys

from paths import *
from snake import *


class App:
    def __init__(self):
        pygame.init()
        self.cell_number = 20
        self.cell_size = 40
        self.screen_size = (self.cell_number * self.cell_size, self.cell_number * self.cell_size)
        self.state = 'options'
        self.snake = None

    def draw_background(self, surface):
        surface.fill(colors['board_grass_1'])
        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size,
                                                 self.cell_size)
                        pygame.draw.rect(surface, colors['board_grass_2'], grass_rect)
            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size,
                                                 self.cell_size)
                        pygame.draw.rect(surface, colors['board_grass_2'], grass_rect)

    def draw(self, surface):

        self.snake.draw_snake(surface)

    def game(self):
        pygame.init()
        icon = pygame.image.load(icons_paths['snake'])
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Snake', 'Snake')
        screen = pygame.display.set_mode(self.screen_size)
        self.snake = Snake(self.cell_size)
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, 150)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE and self.state == 'game':
                    self.snake.move_snake()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and app.snake.direction.y != 1:
                        app.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and app.snake.direction.y != -1:
                        app.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and app.snake.direction.x != 1:
                        app.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and app.snake.direction.x != -1:
                        app.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_ESCAPE and self.state == 'options':
                        self.state = 'game'
                    elif event.key == pygame.K_ESCAPE and self.state == 'game':
                        self.state = 'options'

            self.draw_background(screen)
            if self.state == 'game':
                self.draw(screen)
            pygame.display.update()
            clock.tick(60)


app = App()
app.game()
