import random
import sys

import pygame
from pygame import Vector2


class Prey:
    def __init__(self):
        self.randomize()

    def draw(self):
        prey_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size,
                                cell_size)
        pygame.draw.rect(screen, (126, 166, 114), prey_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)


class Snake:
    life = 100

    def __init__(self, name):
        self.name = name
        self.body = [Vector2(5, 1), Vector2(5, 2), Vector2(5, 3)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (48, 105, 152), rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]


class App:
    def __init__(self):
        self.snake = Snake('Python')
        self.prey = Prey()

    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw(self):
        self.prey.draw()
        self.snake.draw_snake()

    def check_collision(self):
        if self.snake.body[0] == self.prey.position:
            self.prey.randomize()
            self.snake.new_block = True


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
test_surface = pygame.Surface((100, 200))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

app = App()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            app.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and app.snake.direction.y != 1:
                app.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and app.snake.direction.y != -1:
                app.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and app.snake.direction.x != 1:
                app.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and app.snake.direction.x != -1:
                app.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    app.draw()
    pygame.display.update()
    clock.tick(60)
