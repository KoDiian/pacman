import pygame
import random

class Pac_Gomme:
    def __init__(self, screen, laby, tilesize, gomme_color):
        self.color = gomme_color
        self.screen = screen
        self.laby = laby
        self.tilesize = tilesize
        self.pac_gomme = []
        self.nb_pac_gomme = 0
        self.points = [
            (),
            (),
            (),
            ()
        ]


    def placement(self):
        width, height = self.laby.getSize()
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        while self.laby.hit_box(x, y):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        self.pac_gomme.append((x, y))
    
    def afficher(self):
        for gomme in self.pac_gomme:
            pygame.draw.circle(self.screen, (0, 0, 255), (gomme[0] * self.tilesize + self.tilesize // 2, gomme[1] * self.tilesize + self.tilesize // 2), self.tilesize // 4)

    def ramasser(self, player_pos):
        for gomme in self.pac_gomme:
            if (player_pos.x, player_pos.y) == gomme:
                self.pac_gomme.remove(gomme)
                self.nb_pac_gomme += 1
                return True
        return False