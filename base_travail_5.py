import pygame
from utils import Pos
from pac import *
from labyrinthe import Labyrinthe
from pac_gomme import *
from utils import convert_data
from fantome import Fantome

pygame.init()

# Constantes
tilesize = 32  # taille d'une tuile IG
size = (20, 10)  # taille du monde 20/10 ou 19/22
size_level1 =  (20, 10)
size_level2 = (19, 22)
fps = 30  # fps du jeu
player_speed = 200  # vitesse du joueur
next_move = 0  # tic avant déplacement
pacman_powered_up = False 

# Couleurs
color = {
    "ground_color": "#000000",
    "player_color": "#ffff08",
    "wall_color": "#0000FF",
    "gomme_color": "#00FFFF",
}

# Texte
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont(None, 48)




level1 = "data/laby-01.dat"
level2 = "data/laby-02.dat"
level = level1

score = 0
hall_of_frame = "score.txt"


player_pos_level1 = Pos(10, 7)
player_pos_level2 = Pos(9, 18)
player_pos = player_pos_level1

keys = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}

running = True



# Premier level
laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])



screen = pygame.display.set_mode((size[0] * tilesize, size[1] * tilesize))
clock = pygame.time.Clock()
dt = 0

fantomes = []
for _ in range(4):
    while True:
        x, y = random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)
        if not laby.hit_box(x, y):
            fantomes.append(Fantome(x, y))
            break

number_move = 0

bonus_number = 0
matrice = [[0] * size[0] for _ in range(size[1])]
with open(level) as file:
    firstline = file.readline()
    sndline = file.readline()
    lines = [line.rstrip() for line in file]
    for i in range(len(lines)):
        tmp = lines[i]
        tmp_list = tmp.split(',')
        for j in range(len(tmp_list)):
            matrice[i][j] = convert_data(tmp_list[j])
            if matrice[i][j] == 0:  # Si la case n'est pas un mur
                bonus_number += 1

gomme = Pac_Gomme(screen, laby, tilesize, color["gomme_color"])
for _ in range(5):
    gomme.placement()



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
              # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['DOWN'] == 1:
            new_y += 1
            number_move += 1
            if new_y >= size[1]:  # Si PACMAN atteint le bord inférieur
                new_y = 0  # PACMAN réapparaît en haut
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['LEFT'] == 1:
            new_x -= 1
            number_move += 1
            if new_x < 0:  # Si PACMAN atteint le bord gauche
                new_x = size[0] - 1  # PACMAN réapparaît à droite
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['RIGHT'] == 1:
            new_x += 1
            number_move += 1
            if new_x >= size[0]:  # Si PACMAN atteint le bord droit
                new_x = 0  # PACMAN réapparaît à gauche
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

    #
    # Détection de collision avec les fantômes
    #
    for fantome in fantomes:
        if (player_pos.x, player_pos.y) == (fantome.x, fantome.y):
            if not pacman_powered_up:
                running = False
                print("Vous avez perdu !")
            else:
                fantomes.remove(fantome)
                score += 50
                print("Fantôme mangé ! Score +50")

    # Vérifier si la minuterie de l'alimentation de PACMAN a expiré
    if pacman_powered_up:
        current_time = pygame.time.get_ticks()
        if current_time - power_up_timer >= 15000:  # 15 secondes en millisecondes
            pacman_powered_up = False

    #
    # Déplacement aléatoire des fantômes
    #
    for fantome in fantomes:
        fantome.move_randomly(laby)

    #
    # Vérification et réapparition des fantômes
    #
    Fantome.check_respawn()

        

 



    #
    # Affichage des différents composants graphiques
    #
    screen.fill(color["ground_color"])
    

    laby.draw(screen, tilesize)


    if gomme.ramasser(player_pos):
        score += 100
        # Déclencher l'état de PACMAN alimenté et la minuterie
        pacman_powered_up = True
        power_up_timer = pygame.time.get_ticks()
    pygame.draw.circle(screen, color["player_color"], (player_pos.x * tilesize + tilesize // 2, player_pos.y * tilesize + tilesize // 2), tilesize // 2)

    gomme.afficher()

    score_text = font.render("Score: " + str(score), True, BLACK) 
    screen.blit(score_text, (10, 2)) 
    move_text = font.render("Move: " + str(number_move), True, BLACK)
    screen.blit(move_text, (200, 2))
    # Affichage des fantômes
    for fantome in fantomes:
        fantome.draw(screen, tilesize)

    # Affichage d'un message si le joueur a perdu
    if not running:
        lost_text = font.render("Vous avez perdu !", True, WHITE)
        screen.blit(lost_text, (size[0] * tilesize // 2 - 150, size[1] * tilesize // 2 - 24))
        print("Vous avez perdu !")
  

    # Affichage des modifications du screen_view
    pygame.display.flip()
    # Gestion fps
    dt = clock.tick(fps)

    if bonus_number == 0:
        running = False
        
if bonus_number == 0:
    if level == level1:
        level = level2
        size = size_level2
        player_pos = player_pos_level2
        running = True 
    else:
        pygame.quit()



# Second level
laby = Labyrinthe(size[0], size[1])
laby.load_from_file(level)
laby.set_color(color["wall_color"])



screen = pygame.display.set_mode((size[0] * tilesize, size[1] * tilesize))
clock = pygame.time.Clock()
dt = 0


number_move = 0

bonus_number = 0
matrice = [[0] * size[0] for _ in range(size[1])]
with open(level) as file:
    firstline = file.readline()
    sndline = file.readline()
    lines = [line.rstrip() for line in file]
    for i in range(len(lines)):
        tmp = lines[i]
        tmp_list = tmp.split(',')
        for j in range(len(tmp_list)):
            matrice[i][j] = convert_data(tmp_list[j])
            if matrice[i][j] == 0:  # Si la case n'est pas un mur
                bonus_number += 1

gomme = Pac_Gomme(screen, laby, tilesize, color["gomme_color"])
for _ in range(5):
    gomme.placement()

for _ in range(4):
    while True:
        x, y = random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)
        if not laby.hit_box(x, y):
            fantomes.append(Fantome(x, y))
            break


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
              # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['DOWN'] == 1:
            new_y += 1
            number_move += 1
            if new_y >= size[1]:  # Si PACMAN atteint le bord inférieur
                new_y = 0  # PACMAN réapparaît en haut
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['LEFT'] == 1:
            new_x -= 1
            number_move += 1
            if new_x < 0:  # Si PACMAN atteint le bord gauche
                new_x = size[0] - 1  # PACMAN réapparaît à droite
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1 
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        
        elif keys['RIGHT'] == 1:
            new_x += 1
            number_move += 1
            if new_x >= size[0]:  # Si PACMAN atteint le bord droit
                new_x = 0  # PACMAN réapparaît à gauche
               # Vérification du déplacement du joueur
            if laby.hit_box(new_x, new_y):
                number_move -=1
            else:
                player_pos.x, player_pos.y = new_x, new_y
                next_move -= player_speed

                # Gestion de la collision avec les bonus
                if laby.process_bonus_collision(player_pos.x, player_pos.y):
                    score += 1
                    bonus_number -= 1
                else:
                    score -=1

        #
    # Détection de collision avec les fantômes
    #
    for fantome in fantomes:
        if (player_pos.x, player_pos.y) == (fantome.x, fantome.y):
            if not pacman_powered_up:
                running = False
                print("Vous avez perdu !")
            else:
                fantomes.remove(fantome)
                score += 50
                print("Fantôme mangé ! Score +50")

    # Vérifier si la minuterie de l'alimentation de PACMAN a expiré
    if pacman_powered_up:
        current_time = pygame.time.get_ticks()
        if current_time - power_up_timer >= 15000:  # 15 secondes en millisecondes
            pacman_powered_up = False

    #
    # Déplacement aléatoire des fantômes
    #
    for fantome in fantomes:
        fantome.move_randomly(laby)

    #
    # Vérification et réapparition des fantômes
    #
    Fantome.check_respawn()       

      



    #
    # Affichage des différents composants graphiques
    #
    screen.fill(color["ground_color"])
    

    laby.draw(screen, tilesize)


    if gomme.ramasser(player_pos):
        score += 100
        # Déclencher l'état de PACMAN alimenté et la minuterie
        pacman_powered_up = True
        power_up_timer = pygame.time.get_ticks()
    pygame.draw.circle(screen, color["player_color"], (player_pos.x * tilesize + tilesize // 2, player_pos.y * tilesize + tilesize // 2), tilesize // 2)

    gomme.afficher()

    score_text = font.render("Score: " + str(score), True, BLACK) 
    screen.blit(score_text, (10, 2)) 
    move_text = font.render("Move: " + str(number_move), True, BLACK)
    screen.blit(move_text, (200, 2))

    # Affichage des fantômes
    for fantome in fantomes:
        fantome.draw(screen, tilesize)

    # Affichage d'un message si le joueur a perdu
    if not running:
        lost_text = font.render("Vous avez perdu !", True, WHITE)
        screen.blit(lost_text, (size[0] * tilesize // 2 - 150, size[1] * tilesize // 2 - 24))
        print("Vous avez perdu !")
  

    # Affichage des modifications du screen_view
    pygame.display.flip()
    # Gestion fps
    dt = clock.tick(fps)

    if bonus_number == 0:
        with open(hall_of_frame, "a") as fichier:
            fichier.write("\n")
            fichier.write(str(score))
        running = False

print("Votre score est de ",score)
print("Votre nombre de pas est de ",number_move)


pygame.quit()
