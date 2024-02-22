import pygame
class Pacman:
    def __init__(self):
        self.body = [(200, 200)]
        self.direction = (1, 0)

    def move(self, tilesize, size):
        width = size[0]
        height = size[1]
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx * tilesize) % width, (y + dy * tilesize) % height)
        self.body.insert(0, new_head)
    
    def draw(self, surface, tilesize):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255,0), (segment[0], segment[1], tilesize, tilesize))