import pygame
from projectile import Projectile
import animation

# creer une classe qui va representer notre joueur
class Player(animation.AnimateSprite):

    def __init__(self, game):
        # faire heriter la classe Sprite dans la fonction init
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 500

        # self.image = pygame.image.load('Assets/player.png')

    def damage(self, amount):
        # infliger les degats
        if self.health - amount > amount:
            self.health -= amount
        else:
            # mettre fin au jeu quand la vie du joueur est à 0
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def update_health_bar(self, surface):
        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (110, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 7])


    def launch_projectile(self):
        # creer une nouvell instance de la classe Projectile
        self.all_projectiles.add(Projectile(self))
        # demarrer l'animation du lancer projectile
        self.start_animation()
        # joueur le son
        self.game.sound_manager.play('tir')

    def move_right(self):
        # si le joueur n'est pas en collision avec un monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def pause_player(self):
        self.rect.x = self.rect.x
