import pygame
from pygame import Vector2


class Snake:
    def __init__(self, cell_size):
        self.body = [Vector2(5, 1), Vector2(5, 2), Vector2(5, 3)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.cell_size = cell_size
        self.head = None
        self.tail = None
        # Snake body:
        self.head_up = pygame.image.load('./graphics/snake_body/head_up.png')
        self.head_down = pygame.image.load('./graphics/snake_body/head_down.png')
        self.head_left = pygame.image.load('./graphics/snake_body/head_left.png')
        self.head_right = pygame.image.load('./graphics/snake_body/head_right.png')

        self.tail_up = pygame.image.load('./graphics/snake_body/tail_up.png')
        self.tail_down = pygame.image.load('./graphics/snake_body/tail_down.png')
        self.tail_left = pygame.image.load('./graphics/snake_body/tail_left.png')
        self.tail_right = pygame.image.load('./graphics/snake_body/tail_right.png')

        self.body_vertical = pygame.image.load('./graphics/snake_body/body_vertical.png')
        self.body_horizontal = pygame.image.load('./graphics/snake_body/body_horizontal.png')
        self.body_tr = pygame.image.load('./graphics/snake_body/body_tr.png')
        self.body_tl = pygame.image.load('./graphics/snake_body/body_tl.png')
        self.body_br = pygame.image.load('./graphics/snake_body/body_br.png')
        self.body_bl = pygame.image.load('./graphics/snake_body/body_bl.png')

    def draw_snake(self, surface):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * self.cell_size)
            y_pos = int(block.y * self.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)

            if index == 0:
                surface.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                surface.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    surface.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    surface.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        surface.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        surface.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        surface.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        surface.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def up(self):
        self.direction = Vector2(0, -1)

    def down(self):
        self.direction = Vector2(0, 1)

    def right(self):
        self.direction = Vector2(1, 0)

    def left(self):
        self.direction = Vector2(-1, 0)

    def reset(self):
        self.body = [Vector2(5, 1), Vector2(5, 2), Vector2(5, 3)]
        self.direction = Vector2(1, 0)
