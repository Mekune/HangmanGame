import random
import pygame
import time

# Paramètres d'affichage
pygame.init()
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Fonction pour configurer la fenêtre
def page(taille_x, taille_y, nom):
    fenetre = pygame.display.set_mode((taille_x, taille_y))
    fonte = pygame.font.Font("font/OMORI_GAME.ttf", 36)
    fontemini = pygame.font.Font("font/OMORI_GAME.ttf", 22)
    fenetre.fill(NOIR)
    pygame.display.set_caption(nom)
    return fonte,fontemini, fenetre

def playSong(nom):
    son = pygame.mixer.Sound(f"song/{nom}.mp3")
    son.play()
    canal = pygame.mixer.Channel(0)
    return canal,son

def afficherTexte(nom,couleur,x,y,fonte,fenetre):
    texte_menu = fonte.render(nom, True, couleur)
    fenetre.blit(texte_menu, (x, y))


def afficherRectangle(x,y,largeur,hauteur,couleur,fenetre,nombre):
    rectanglenoir = pygame.Rect(x,y,largeur,hauteur)
    pygame.draw.rect(fenetre,couleur,rectanglenoir,nombre)
    return rectanglenoir

# Fonction du menu
def menu():
    pygame.mixer.init()
    canal, son = playSong("Omori_title")
    title = [pygame.image.load(f"picture/{index}.png") for index in range(0, 3)]
    setTimeSprite(350)
    curIndex = 0

    fonte,fontemini,fenetre = page(800, 552, "Menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playSong("exit")
                time.sleep(0.4)
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    playSong("play")
                    son.stop()
                    hangman()
                elif exit_button.collidepoint(event.pos):
                    playSong("exit")
                    time.sleep(0.4)
                    pygame.quit()
            if event.type == CHANGE_IMAGE_EVENT:
                curIndex = (curIndex + 1) % len(title)
        if not canal.get_busy():
            son.play()
        
        ShowCorrectFrame(title ,curIndex)
        fenetre.blit(title[curIndex],(90,0))
        afficherTexte("HANGMAN GAME !",BLANC,300,50,fonte,fenetre)
        afficherTexte("* Omori version",BLANC,350,85,fontemini,fenetre)
        afficherTexte("JOUER",BLANC,170,490,fonte,fenetre)
        afficherTexte("EXIT",BLANC,630,490,fonte,fenetre)
        exit_button = afficherRectangle(610,480,100,50,BLANC,fenetre,2)
        play_button = afficherRectangle(155,480,100,50,BLANC,fenetre,2)
        pygame.display.flip()

# Fonction du jeu Hangman
def hangman():
    canal, son = playSong("metronome")
    with open("liste_mot", "r") as fichier:
        liste_mot = fichier.read().splitlines()
    mot = random.choice(liste_mot)
    mot = mot.upper()
    fonte,fontemini, fenetre = page(800, 552, "Hangman Game")
    lettre_in_mot = []
    lettre_notin_mot = []
    point = 10
    erreur = 0
    reponse = ""
    letterdouble = False
    partie_terminee = False  # Variable pour suivre si la partie est terminée

    while not partie_terminee:
        if not canal.get_busy():
            son.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playSong("exit")
                time.sleep(0.4)
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    reponse = chr(event.key).upper()
                    if reponse in lettre_notin_mot or reponse in lettre_in_mot:
                        letterdouble = True
                    elif reponse in mot:
                        playSong("letter")
                        lettre_in_mot.append(reponse)
                        letterdouble = False
                    else:
                        playSong("notletter")
                        lettre_notin_mot.append(reponse)
                        point -= 1
                        erreur += 1
                        letterdouble = False
        if letterdouble:
            afficherTexte("lettre deja choisit",BLANC,75,100,fonte,fenetre)
        mot_cache = affichage_mot_cachee(mot, lettre_in_mot)
        afficherTexte(mot_cache,BLANC,300,500,fonte,fenetre)
        afficherTexte(f"Points restants : {point}",BLANC,80,10,fonte,fenetre)
        
        dessiner_pendu(erreur, fenetre)
        afficherRectangle(0,0,350,50,BLANC,fenetre,2)
        afficherRectangle(0,55,350,395,BLANC,fenetre,2)
        afficherRectangle(0,455,800,90,BLANC,fenetre,2)
        afficherRectangle(355,0,445,450,BLANC,fenetre,2)
        if point <= 0:
            son.stop()
            playSong("loose")
            image = pygame.image.load("picture/something.webp")
            image = pygame.transform.scale(image, (75,200))
            fenetre.blit(image,(490,150))
            afficherTexte("Perdu !",BLANC,125,75,fonte,fenetre)
            afficherTexte(f"le mot etait : {mot}",BLANC,25,250,fonte,fenetre)
        if "_" not in mot_cache:
            son.stop()
            playSong("win")
            afficherTexte("Gagne !",BLANC,125,75,fonte,fenetre)
        if lettre_notin_mot:
            liste_lettre = str(lettre_notin_mot)
            afficherTexte(liste_lettre,BLANC,400,10,fonte,fenetre)
        pygame.display.flip()
        fenetre.fill(NOIR)
        if point <= 0:
            time.sleep(4)
            partie_terminee = True
        if "_" not in mot_cache:
            time.sleep(4)
            partie_terminee = True






# Fonction pour afficher le mot masqué
def affichage_mot_cachee(mot, lettre_trouvees):
    mot_cache = ""
    for letter in mot:
        if letter == " ":
            mot_cache += " "
        elif (letter in lettre_trouvees):
            mot_cache += letter
        else:
            mot_cache += " _"
    return mot_cache

# Fonction pour dessiner le pendu
def dessiner_pendu(erreur, fenetre):
    pendu = [
        [(525, 100), (525, 150)],  # Corde
        [(525, 100), (625, 100)],  # Poteau horizontal
        [(626, 400), (626, 100)],  # Poteau vertical
        [(525, 400), (675, 400)],  # Base
        [(525, 175)],               # tete
        [(500, 200), (500, 275),(550, 200), (550, 275),(500,275),(550,275)],   # corps
        [(515, 215), (515, 250),(535, 215), (535, 250)],   # bras
        [(515, 275), (515, 330),(535, 275), (535, 330)],   # jambes
        [(510, 170), (520, 170),(535,170),(545,170)],   # yeux
        [(525, 300), (550, 350)],   # bouche
    ]

    for i in range(erreur):
        if i == 4:
            pygame.draw.circle(fenetre, BLANC, pendu[i][0], 35)
            pygame.draw.circle(fenetre, NOIR, pendu[i][0], 30)
        elif i == 5:
            pygame.draw.line(fenetre, BLANC, pendu[i][0], pendu[i][1], 4)
            pygame.draw.line(fenetre, BLANC, pendu[i][2], pendu[i][3], 4)
            pygame.draw.line(fenetre, BLANC, pendu[i][4], pendu[i][5], 4)
        elif i == 6 or i == 7:
            pygame.draw.line(fenetre, BLANC, pendu[i][0], pendu[i][1], 4)
            pygame.draw.line(fenetre, BLANC, pendu[i][2], pendu[i][3], 4)
        elif i == 8 :
                pygame.draw.line(fenetre, BLANC, pendu[i][0], pendu[i][1], 2)
                pygame.draw.line(fenetre, BLANC, pendu[i][2], pendu[i][3], 2)
        else:
            pygame.draw.line(fenetre, BLANC, pendu[i][0], pendu[i][1], 4)

def ShowCorrectFrame(Sprites,index):
    for i, Frame in enumerate(Sprites):
        if i == index:
            Frame.set_alpha(255)  # Rendre l'image visible
        else:
            Frame.set_alpha(0)  # Rendre l'image invisible

CHANGE_IMAGE_EVENT = 0
def setTimeSprite(Time):
    global CHANGE_IMAGE_EVENT
    CHANGE_IMAGE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_IMAGE_EVENT, Time)

def getCurTimeSprite():
    global CHANGE_IMAGE_EVENT
    return CHANGE_IMAGE_EVENT



menu()
