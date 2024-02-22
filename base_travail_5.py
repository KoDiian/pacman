import pygame
import random
from utils import convert_data
from grid import Grid
from utils import Pos
from pac import *

class Labyrinthe:
    # constructeur
    def __init__(self, sizeX, sizeY, main_loop=None):
        """sizeX, sizeY désignent la taille du labyrinthe sur l'axe (x,y)"""
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.version = ""
        self.author = ""
        # attention création d'une matrice en Y X
        self.matrice = [[0] * self.sizeX for _ in range(self.sizeY)]
        self.color = (0, 0, 255)  # Couleur par défaut des murs en bleu
        self.main_loop = main_loop  # Référence à la boucle principale du jeu

    def set_color(self, v):
        """Fixe la couleur pour dessiner les murs"""
        self.color = v

    def display_on_console(self):
        """Sortie console du labyrinthe"""
        for j in range(self.sizeY):
            for i in range(self.sizeX):
                # rappel: matrice en Y,X
                print(self.matrice[j][i], end="")
            print()

    def get_matrice(self):
        """renvoie la matrice associée au labyrinthe"""
        return self.matrice

    def getXY(self, i, j):
        """Renvoie la case (i,j) du labyrinthe sur l'axe (x,y)"""
        return self.matrice[j][i]

    def setXY(self, i, j, v):
        """Modifie par v la case (i,j) sur l'axe (x,y)"""
        self.matrice[j][i] = v

    def getSize(self):
        """Renvoie la taille (x,y) du labyrinthe"""
        return (self.sizeX, self.sizeY)

    def load_from_file(self, filename):
        """Charge un labyrinthe d'un fichier texte"""
        with open(filename) as file:
            # lecture du cartouche du labyrinthe
            # 1) vérification du type de fichier
            firstline = file.readline()
            firstline = firstline.rstrip()
            firstline = firstline.split(',')
            if firstline[0] != "map":
                print("mauvais fichier")
                return
            self.version = firstline[1]
            self.author = firstline[2]
            # 2) vérification de la taille du labyrinthe
            snd_line = file.readline()
            snd_line = snd_line.rstrip()
            snd_line = snd_line.split(',')
            if int(snd_line[0]) != self.sizeX or int(snd_line[1]) != self.sizeY:
                print("dimensions non cohérentes")
                return
            # lecture des données du labyrinthe
            lines = [line.rstrip() for line in file]
        for i in range(len(lines)):
            tmp = lines[i]
            tmp_list = tmp.split(',')
            for j in range(len(tmp_list)):
                tmp_list[j] = convert_data(tmp_list[j])
            self.matrice[i] = tmp_list

    def hit_box(self, x, y):
        """indique si l'élément (x,y) est un mur"""
        if x >= self.sizeX or x < 0 or y < 0 or y >= self.sizeY:
            return True
        if self.matrice[y][x] == 1:
            print("Vous avez perdu")  # Si le joueur touche un mur, on imprime "perdu" dans la console
            if self.main_loop:
                self.main_loop.running = False  # Ferme le jeu si la boucle principale est définie
            return True
        return False

    def draw(self, screen, tilesize):
        """dessine le labyrinthe sur la fenètre screen"""
        for j in range(self.sizeY):
            for i in range(self.sizeX):
                if self.matrice[j][i] == 1:
                    pygame.draw.rect(screen, self.color, (i * tilesize, j * tilesize, tilesize, tilesize))

# pygame setup
pygame.init()

# Constantes
tilesize = 32  # taille d'une tuile IG
size = (20, 10)  # taille du monde
fps = 30  # fps du jeu
player_speed = 150  # vitesse du joueur
next_move = 0  # tic avant déplacement

# Couleurs
color = {
    "ground_color": "#EDDACF",
    "grid_color": "#7F513D",
    "player_color": "#ffff08",
    "wall_color": "#0000FF"
}

level = "data/laby-01.dat"

laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])

grid = Grid(size[0], size[1], tilesize)
grid.set_color(color["grid_color"])

screen = pygame.display.set_mode((size[0] * tilesize, size[1] * tilesize))
clock = pygame.time.Clock()
running = True
dt = 0

show_grid = True
show_pos = False

keys = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}

player_pos = Pos(0, 1)

# Tour de boucle, pour chaque FPS
while running:

    
    # Lecture clavier / souris
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                keys['UP'] = 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys['DOWN'] = 1
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                keys['LEFT'] = 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys['RIGHT'] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                keys['UP'] = 0
                next_move = 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys['DOWN'] = 0
                next_move = 1
            if event.key == pygame.K_q or event.key == pygame.K_LEFT:
                keys['LEFT'] = 0
                next_move = 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys['RIGHT'] = 0
                next_move = 1

            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_g:
                show_grid = not show_grid
            if event.key == pygame.K_p:
                show_pos = not show_pos
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print("mouse_pos:", pos)

    #
    # Gestion des déplacements
    #

    next_move += dt
    if next_move > 0:
        new_x, new_y = player_pos.x, player_pos.y
        if keys['UP'] == 1:
            new_y -= 1
            if new_y < 0:  # Si PACMAN atteint le bord supérieur
                new_y = size[1] - 1  # PACMAN réapparaît en bas
        elif keys['DOWN'] == 1:
            new_y += 1
            if new_y >= size[1]:  # Si PACMAN atteint le bord inférieur
                new_y = 0  # PACMAN réapparaît en haut
        elif keys['LEFT'] == 1:
            new_x -= 1
            if new_x < 0:  # Si PACMAN atteint le bord gauche
                new_x = size[0] - 1  # PACMAN réapparaît à droite
        elif keys['RIGHT'] == 1:
            new_x += 1
            if new_x >= size[0]:  # Si PACMAN atteint le bord droit
                new_x = 0  # PACMAN réapparaît à gauche

        # Vérification du déplacement du joueur                                    
        if laby.hit_box(new_x, new_y):
            print("")  # Affichage dans la console
            running = False  # Arrêt du jeu si le joueur touche un mur
        else:
            player_pos.x, player_pos.y = new_x, new_y
            next_move -= player_speed

        if show_pos:
            print("pos: ", player_pos)

    #
    # Affichage des différents composants graphiques
    #
    screen.fill(color["ground_color"])

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

    pygame.draw.circle(screen, color["player_color"], (player_pos.x * tilesize + tilesize // 2, player_pos.y * tilesize + tilesize // 2), tilesize // 2)

    # Affichage des modifications du screen_view
    pygame.display.flip()
    # Gestion fps
    dt = clock.tick(fps)

pygame.quit()
