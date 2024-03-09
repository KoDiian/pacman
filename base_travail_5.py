import pygame
from utils import Pos
from pac import *
from labyrinthe import Labyrinthe
from pac_gomme import *

pygame.init()

# Constantes
tilesize = 32  # taille d'une tuile IG
size = (19, 22)  # taille du monde
fps = 30  # fps du jeu
player_speed = 200  # vitesse du joueur
next_move = 0  # tic avant déplacement

# Couleurs
color = {
    "ground_color": "#000000",
    "player_color": "#ffff08",
    "wall_color": "#0000FF",
    "gomme_color": "#00FFFF",
}



level = "data/laby-02.dat"

laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])



screen = pygame.display.set_mode((size[0] * tilesize, size[1] * tilesize))
clock = pygame.time.Clock()
running = True
dt = 0



keys = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}

player_pos = Pos(9, 18)

pacman = Pacman(color["player_color"], (9,19))

number_move = 0
gomme = Pac_Gomme(screen, laby, tilesize, color["gomme_color"])
for _ in range(5):
    gomme.placement()

score = 0

# Tour de boucle, pour chaque FPS
while running:

    # Lecture clavier / souris
    for event in pygame.event.get():
        # Si on clique sur la croix rouge le jeu se ferme
        if event.type == pygame.QUIT:
            running = False

        # Verifie si une touche est appuyé
        if event.type == pygame.KEYUP:
            # Si la touche echap est appuyé le jeu se ferme
            if event.key == pygame.K_ESCAPE:
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

            


    #
    # Gestion des déplacements
    #

    next_move += dt
    if next_move > 0:
        new_x, new_y = player_pos.x, player_pos.y
        if keys['UP'] == 1:
            new_y -= 1
            number_move += 1
            if new_y < 0:  # Si PACMAN atteint le bord supérieur
                new_y = size[1] - 1  # PACMAN réapparaît en bas
        elif keys['DOWN'] == 1:
            new_y += 1
            number_move += 1
            if new_y >= size[1]:  # Si PACMAN atteint le bord inférieur
                new_y = 0  # PACMAN réapparaît en haut
        elif keys['LEFT'] == 1:
            new_x -= 1
            number_move += 1
            if new_x < 0:  # Si PACMAN atteint le bord gauche
                new_x = size[0] - 1  # PACMAN réapparaît à droite
        elif keys['RIGHT'] == 1:
            new_x += 1
            number_move += 1
            if new_x >= size[0]:  # Si PACMAN atteint le bord droit
                new_x = 0  # PACMAN réapparaît à gauche

        # Vérification du déplacement du joueur
        if laby.hit_box(new_x, new_y):
            number_move -=1
            running = True  
        else:
            player_pos.x, player_pos.y = new_x, new_y
            next_move -= player_speed

            # Gestion de la collision avec les bonus
            if laby.process_bonus_collision(player_pos.x, player_pos.y):
                # Si le joueur a ramassé un bonus, faites quelque chose, comme augmenter son score
                # Par exemple, ici, j'augmente le score de 1
                score += 1



    #
    # Affichage des différents composants graphiques
    #
    screen.fill(color["ground_color"])
    

    laby.draw(screen, tilesize)


    if gomme.ramasser(player_pos):
        score += 100
    pygame.draw.circle(screen, color["player_color"], (player_pos.x * tilesize + tilesize // 2, player_pos.y * tilesize + tilesize // 2), tilesize // 2)

    gomme.afficher()
    
    # Affichage des modifications du screen_view
    pygame.display.flip()
    # Gestion fps
    dt = clock.tick(fps)

print("Votre score est de ",score)
print("Votre nombre de pas est de ",number_move)
pygame.quit()
