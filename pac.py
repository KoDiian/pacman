import pygame
from labyrinthe import Labyrinthe
import time
class Pacman:
    def __init__(self, color, pos):
        self.color_body = color
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.direction ='UP'
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, screen, tilesize):
        pygame.draw.circle(screen, self.color_body, (self.pos_x * tilesize + tilesize // 2, self.pos_y * tilesize + tilesize // 2), tilesize // 2)

    def move(self):
        if self.direction == 'RIGHT':
            self.pos_x += 1
        elif self.direction == 'LEFT':
            self.pos_x -= 1
        elif self.direction == 'UP':
            self.pos_y -= 1
        elif self.direction == 'DOWN':
            self.pos_y += 1

    def change_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                self.direction = 'UP'
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.direction = 'DOWN'
            elif event.key == pygame.K_q or event.key == pygame.K_LEFT:
                self.direction = 'LEFT'
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.direction = 'RIGHT'


    def check_wall_collision(self, labyrinthe):
        next_x, next_y = self.pos_x, self.pos_y

        # Vérifie si la prochaine position de Pacman est un mur dans le labyrinthe
        if labyrinthe.hit_box(next_x, next_y):
            # Collision avec un mur
            return True
        else:
            # Pas de collision avec un mur
            return False
        
    def move_back(self):
        # Annule le dernier mouvement de Pacman en le ramenant à sa position précédente
        if self.direction == 'RIGHT':
            self.pos_x -= 1
        elif self.direction == 'LEFT':
            self.pos_x += 1
        elif self.direction == 'UP':
            self.pos_y += 1
        elif self.direction == 'DOWN':
            self.pos_y -= 1