import pygame
from utils import Pos
class Pacman:
    def __init__(self, color, pos):
        self.body = [(200, 200)]
        self.direction = (1, 0)
        self.color_body = color
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def move(self, tilesize, size):
        width = size[0]
        height = size[1]
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx * tilesize) % width, (y + dy * tilesize) % height)
        self.body.insert(0, new_head)
    
    def draw(self, screen, tilesize):
        pygame.draw.circle(screen, self.color_body, (self.pos_x * tilesize + tilesize // 2, self.pos_y * tilesize + tilesize // 2), tilesize // 2)