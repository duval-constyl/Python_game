import sys

import pygame
import math
from player import Player
from monster import Monster, Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager


# creer une classe qui va representer notre jeu
class Game:

    def __init__(self):
        # definir si notre jeu a commencé
        self.is_playing = False
        # definir une pause
        self.is_pause = False
        self.pause_image = pygame.image.load("Assets/pause.png")
        self.pause_image = pygame.transform.scale(self.pause_image, (40, 40))
        self.pause_image_rect = self.pause_image.get_rect()
        # generer notre joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # gerer le son
        self.sound_manager = SoundManager()
        # generer l'evenement
        self.comet_event = CometFallEvent(self)
        # groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        # mettre le score à 0
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def add_score(self, points):
        self.score += points

    def pause(self, screen, clock):
        self.is_pause = True
        self.sound_manager.play('start')
        self.player.pause_player()

        for monster in self.all_monsters:
            monster.pause_monster()

        for projectile in self.player.all_projectiles:
            projectile.pause_projectile()

        while self.is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_pause = False

            # Afficher le score sur l'écran
            font = pygame.font.Font("Assets/my_font.ttf", 20)
            score_text = font.render(f"Score : {self.score}", 1, (0, 0, 0))
            screen.blit(score_text, (20, 20))

            # Afficher l'image de pause
            screen.blit(self.pause_image, (990, 20))

            pygame.display.flip()
            clock.tick(60)



    def game_over(self):
        # remettre le jeu a neuf
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        # joueur le son
        self.sound_manager.play('game_over')

    def update(self, screen):
        # afficher le score sur l'ecran
        font = pygame.font.Font("Assets/my_font.ttf", 20)
        # font = pygame.font.SysFont("monospace", 16)
        score_text = font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        screen.blit(self.pause_image, (990, 20))

        # appliquer le joueur sur l'interface
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        # actualiser la barre d'evenement du jeu
        self.comet_event.update_bar(screen)

        # actualiser l'animation du joueur
        self.player.update_animation()

        # recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # appliquer l'ensemble des images de mon groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # recuperer les projectiles du joueur
        for monsters in self.all_monsters:
            monsters.forward()
            monsters.update_health_bar(screen)
            monsters.update_animation()

        # appliquer l'ensemble des images de mon groupe de monsters
        self.all_monsters.draw(screen)

        # appliquer l'ensemble des images de mon groupe de comets
        self.comet_event.all_comets.draw(screen)

        # recuperer les comets de notre jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        # verifier si le joueur souhaite aller à gauche ou a droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))
