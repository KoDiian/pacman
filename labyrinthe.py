import pygame
from utils import convert_data
from bonus import Bonus  # Import de la classe Bonus

class Labyrinthe:
    def __init__(self, sizeX, sizeY, main_loop=None):
        """sizeX, sizeY désignent la taille du labyrinthe sur l'axe (x,y)"""
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.version = ""
        self.author = ""
        # Attention création d'une matrice en Y X
        self.matrice = [[0] * self.sizeX for _ in range(self.sizeY)]
        self.color = (0, 0, 255)  # Couleur par défaut des murs en bleu
        self.main_loop = main_loop  # Référence à la boucle principale du jeu
        self.bonuses = []  # Liste pour stocker les bonus

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
        """Renvoie la matrice associée au labyrinthe"""
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
            # Lecture du cartouche du labyrinthe
            # 1) Vérification du type de fichier
            firstline = file.readline()
            firstline = firstline.rstrip()
            firstline = firstline.split(',')
            if firstline[0] != "map":
                print("mauvais fichier")
                return
            self.version = firstline[1]
            self.author = firstline[2]
            # 2) Vérification de la taille du labyrinthe
            snd_line = file.readline()
            snd_line = snd_line.rstrip()
            snd_line = snd_line.split(',')
            if int(snd_line[0]) != self.sizeX or int(snd_line[1]) != self.sizeY:
                print("dimensions non cohérentes")
                return
            # Lecture des données du labyrinthe
            lines = [line.rstrip() for line in file]
        for i in range(len(lines)):
            tmp = lines[i]
            tmp_list = tmp.split(',')
            for j in range(len(tmp_list)):
                self.matrice[i][j] = convert_data(tmp_list[j])
                if self.matrice[i][j] == 0:  # Si la case n'est pas un mur
                    # Créer un bonus à cette position
                    self.bonuses.append(Bonus(j, i))

    def hit_box(self, x, y):
        """Indique si l'élément (x,y) est un mur"""
        if x >= self.sizeX or x < 0 or y < 0 or y >= self.sizeY:
            return True
        if self.matrice[y][x] == 1:
            print("Vous avez perdu")  # Si le joueur touche un mur, on imprime "perdu" dans la console
            if self.main_loop:
                self.main_loop.running = False  # Ferme le jeu si la boucle principale est définie
            return True
        return False

    def draw(self, screen, tilesize):
        """Dessine le labyrinthe sur la fenêtre screen"""
        for j in range(self.sizeY):
            for i in range(self.sizeX):
                if self.matrice[j][i] == 1:
                    pygame.draw.rect(screen, self.color, (i * tilesize, j * tilesize, tilesize, tilesize))
                elif self.matrice[j][i] == 0:  # Si la case n'est pas un mur
                    # Dessiner un bonus à cette position si le bonus est actif
                    for bonus in self.bonuses:
                        if bonus.active and bonus.x == i and bonus.y == j:
                            pygame.draw.rect(screen, (255, 255, 255), (i * tilesize, j * tilesize, tilesize, tilesize))


