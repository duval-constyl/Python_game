import pygame
import math
from game import Game
pygame.init()

# definir une clock
clock = pygame.time.Clock()
FPS = 80


# generer la fenetre du jeu
pygame.display.set_caption("Game Tuto")
screen = pygame.display.set_mode((1080, 720))

# importer de charger l'arriere plan
background = pygame.image.load('Assets/bg.jpg')

#importer notre banniere
banner = pygame.image.load('Assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# importer notre bouton
play_button = pygame.image.load('Assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.3)
play_button_rect.y = math.ceil(screen.get_height() / 2)


# charger le jeu
game = Game()

running = True

# boucle tant que cette condition est vrai
while running:

    # appliquer le background au jeu
    screen.blit(background, (0, -200))

    # verifier si notre jeu a commencé ou non
    if game.is_playing:
        # supprimer le song
        game.sound_manager.remove_sound('start')
        # declencher  les instructions de la partie
        game.update(screen)
    # verifier si notre jeu n'a commencé
    else:
        # ajouter mon ecran de bienvenue
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
        game.sound_manager.play('start', loop=True)

    # mettre à jour l'ecran
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # que l'evenrment est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")

        # detecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # detecter si le touche espace est enclenchée pur lancer le projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()
                else:
                    # mettre le jeu en mode lancé
                    game.start()
                    # joueur le son
                    game.sound_manager.play('click')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verification  si la souris est en collision avec le bouton jouer
            if play_button_rect.collidepoint(event.pos):
                # mettre le jeu en mode lancé
                game.start()
                # joueur le son
                game.sound_manager.play('click')

            if game.pause_image_rect.collidepoint(event.pos):
                # mettre le jeu en mode lancé
                game.pause()
                # joueur le son
                game.sound_manager.play('click')

    # fixer le nmbre de fps sur ma clock
    clock.tick(FPS)
