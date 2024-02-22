import pygame
from grid import Grid
from utils import Pos
from bonus import *
from pac import *
from labyrinthe import Labyrinthe
from pac_gomme import *

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
    "wall_color": "#0000FF",
    "gomme_color": "#00FFFF",
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

number_move = 0
gomme = Pac_Gomme(screen, laby, tilesize, color["gomme_color"])
for _ in range(5):
    gomme.placement()

score = 0

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
            number_move +=1
            if new_y < 0:  # Si PACMAN atteint le bord supérieur
                new_y = size[1] - 1  # PACMAN réapparaît en bas
        elif keys['DOWN'] == 1:
            new_y += 1
            number_move +=1
            if new_y >= size[1]:  # Si PACMAN atteint le bord inférieur
                new_y = 0  # PACMAN réapparaît en haut
        elif keys['LEFT'] == 1:
            new_x -= 1
            number_move +=1
            if new_x < 0:  # Si PACMAN atteint le bord gauche
                new_x = size[0] - 1  # PACMAN réapparaît à droite
        elif keys['RIGHT'] == 1:
            new_x += 1
            number_move +=1
            if new_x >= size[0]:  # Si PACMAN atteint le bord droit
                new_x = 0  # PACMAN réapparaît à gauche

        # Vérification du déplacement du joueur                                    
        if laby.hit_box(new_x, new_y):
            
            running = True  # Arrêt du jeu si le joueur touche un mur
        else:
            player_pos.x, player_pos.y = new_x, new_y
            next_move -= player_speed

        if show_pos:
            print("pos: ", player_pos)

    #
    # Affichage des différents composants graphiques
    #
    screen.fill(color["ground_color"])
    gomme.afficher()

    laby.draw(screen, tilesize)

    if show_grid:
        grid.draw(screen)

    if gomme.ramasser(player_pos):
        score += 100

    pygame.draw.circle(screen, color["player_color"], (player_pos.x * tilesize + tilesize // 2, player_pos.y * tilesize + tilesize // 2), tilesize // 2)

    # Affichage des modifications du screen_view
    pygame.display.flip()
    # Gestion fps
    dt = clock.tick(fps)

print(score)
print(number_move)
pygame.quit()
