import pygame
import random
from utils import convert_data

class Fantome:
    ghost_start_positions = []
    ghost_disappear_times = []

    @classmethod
    def reset_ghost(cls, index):
        cls.ghost_disappear_times[index] = 0

    @classmethod
    def check_respawn(cls):
        global fantomes  # Accéder à la liste fantomes depuis le contexte global
        current_time = pygame.time.get_ticks()
        for i, disappear_time in enumerate(cls.ghost_disappear_times):
            if disappear_time != 0:
                if current_time - disappear_time >= 15000:  # 15 secondes après la disparition
                    x, y = cls.ghost_start_positions[i]
                new_fantome = Fantome(x, y)
                fantomes.append(new_fantome)  # Ajouter le nouveau fantôme à la liste fantomes
                cls.reset_ghost(i)


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # Vitesse de déplacement réduite
        self.start_position = (x, y)
        self.disappeared = False  # Ajouter l'attribut disappeared et l'initialiser à False
        Fantome.ghost_start_positions.append(self.start_position)
        Fantome.ghost_disappear_times.append(0)  # Initialiser le temps de disparition à 0

    def draw(self, screen, tilesize):
        # Dessiner un triangle rouge pour représenter le fantôme
        pygame.draw.polygon(screen, (255, 0, 0), [(self.x * tilesize + tilesize // 2, self.y * tilesize),
                                                  (self.x * tilesize, self.y * tilesize + tilesize),
                                                  ((self.x + 1) * tilesize, self.y * tilesize + tilesize)])
        
    def respawn(self, size):
        self.x, self.y = random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)
        self.disappeared = False

    def move_randomly(self, laby):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)  # Mélanger les directions pour le mouvement aléatoire

        for dx, dy in directions:
            new_x = int(self.x + dx * self.speed)  # Convertir en entier
            new_y = int(self.y + dy * self.speed)  # Convertir en entier

            # Vérifier si la nouvelle position est valide (pas un mur)
            if 0 <= new_x < laby.sizeX and 0 <= new_y < laby.sizeY and not laby.hit_box(new_x, new_y):
                # Vérifier s'il y a un autre fantôme sur la nouvelle position
                if not any(fantome.x == new_x and fantome.y == new_y for fantome in laby.fantomes):
                    # Si la case est libre, déplacer le fantôme
                    self.x = new_x
                    self.y = new_y
                    break  # Sortir de la boucle après avoir trouvé une nouvelle position
