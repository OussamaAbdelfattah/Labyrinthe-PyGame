import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Ajout d'une police de caractères pour le texte
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# Dimensions de la fenêtre
largeur = 800
hauteur = 600

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de labyrinthe")

# Taille des cellules du labyrinthe
taille_cellule = 40

# Classe pour représenter le joueur
class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def deplacer(self, direction, labyrinthe):
        nouvelle_position = (self.x, self.y)

        if direction == "gauche" and self.x > 0 and not labyrinthe.labyrinthe[self.y][self.x - 1]:
            nouvelle_position = (self.x - 1, self.y)
        elif direction == "droite" and self.x < labyrinthe.largeur - 1 and not labyrinthe.labyrinthe[self.y][self.x + 1]:
            nouvelle_position = (self.x + 1, self.y)
        elif direction == "haut" and self.y > 0 and not labyrinthe.labyrinthe[self.y - 1][self.x]:
            nouvelle_position = (self.x, self.y - 1)
        elif direction == "bas" and self.y < labyrinthe.hauteur - 1 and not labyrinthe.labyrinthe[self.y + 1][self.x]:
            nouvelle_position = (self.x, self.y + 1)

        self.x, self.y = nouvelle_position

    def afficher(self):
        pygame.draw.circle(fenetre, rouge, (self.x * taille_cellule + taille_cellule // 2, self.y * taille_cellule + taille_cellule // 2), taille_cellule // 2)

# Classe pour représenter le labyrinthe
class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.labyrinthe = [[True for _ in range(largeur)] for _ in range(hauteur)]
        self.depart = (1, 1)  # Ajout du point de départ
        self.arrivee = (largeur - 2, hauteur - 2)  # Ajout du point d'arrivée
        self.generer()

    def generer(self):
        pile = [(1, 1)]
        while pile:
            x, y = pile[-1]
            self.labyrinthe[y][x] = False
            voisins = []
            if x > 1 and self.labyrinthe[y][x - 2]:
                voisins.append((x - 2, y))
            if x < self.largeur - 2 and self.labyrinthe[y][x + 2]:
                voisins.append((x + 2, y))
            if y > 1 and self.labyrinthe[y - 2][x]:
                voisins.append((x, y - 2))
            if y < self.hauteur - 2 and self.labyrinthe[y + 2][x]:
                voisins.append((x, y + 2))
            if voisins:
                nx, ny = random.choice(voisins)
                self.labyrinthe[(ny + y) // 2][(nx + x) // 2] = False
                pile.append((nx, ny))
            else:
                pile.pop()

    def afficher(self):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if (x, y) == self.depart:
                    pygame.draw.rect(fenetre, vert, (x * taille_cellule, y * taille_cellule, taille_cellule, taille_cellule))
                elif (x, y) == self.arrivee:
                    pygame.draw.rect(fenetre, bleu, (x * taille_cellule, y * taille_cellule, taille_cellule, taille_cellule))
                elif self.labyrinthe[y][x]:
                    pygame.draw.rect(fenetre, blanc, (x * taille_cellule, y * taille_cellule, taille_cellule, taille_cellule))


# Création du joueur et du labyrinthe
joueur = Joueur(1, 1)
labyrinthe = Labyrinthe(largeur // taille_cellule, hauteur // taille_cellule)

# Boucle principale du jeu
en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_LEFT:
                joueur.deplacer("gauche", labyrinthe)
            elif evenement.key == pygame.K_RIGHT:
                joueur.deplacer("droite", labyrinthe)
            elif evenement.key == pygame.K_UP:
                joueur.deplacer("haut", labyrinthe)
            elif evenement.key == pygame.K_DOWN:
                joueur.deplacer("bas", labyrinthe)

    fenetre.fill(noir)
    labyrinthe.afficher()
    joueur.afficher()
    
    # Vérification de l'arrivée du joueur
    if (joueur.x, joueur.y) == labyrinthe.arrivee:
        en_cours = False

        # Affichage du message dans la fenêtre
        message = font.render("Félicitations, vous avez atteint le point d'arrivée!", True, rouge)
        fenetre.blit(message, (50, hauteur // 2 - 15))
        pygame.display.flip()

        # Attente avant de quitter
        pygame.time.delay(3000)  # Attendre 3 secondes (3000 millisecondes)
        pygame.quit()
        sys.exit()

    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
