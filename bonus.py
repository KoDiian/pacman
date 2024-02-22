import pygame

class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True  # Indique si le bonus est actif ou non

    def deactivate(self):
        self.active = False
