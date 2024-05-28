import pygame
import random
import animation


# definir la classe qui va gere la notion de monstre
class Monster(animation.AnimateSprite):

    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.loot_amount = 10
        self.start_animation()

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, 2)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def pause_monster(self):
        self.velocity = 0
        self.default_speed = 0

    def damage(self, amount):
        # infliger les degats
        self.health -= amount

        # supprimer le monstre si son nombre de vie est à zero
        if self.health <= 0:
            # reapparaitre comme un nouveau monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.health = self.max_health
            # ajouter le nombre de points
            self.game.add_score(self.loot_amount)

            # si la barre d'evenement est chargé a son max
            if self.game.comet_event.is_full_loaded():
                # retirer du jeu
                self.game.all_monsters.remove(self)

                # appel de la méthode pour essayer de declencher la pluie de comet
                self.game.comet_event.attempt_fall()

    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):
        # definir un couleur pour la jauge de vie
        bar_color = (110, 210, 46)
        # definir une couleur arriere plan
        back_bar_color = (60, 63, 60)

        # definir la position ainsi que largeur et width
        bar_position = [self.rect.x + 10, self.rect.y - 20, self.health, 5]

        # definir la position de l'arriere plan de la jauge
        back_bar_position = [self.rect.x + 10, self.rect.y - 20, self.max_health, 5]

        # dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)


    def forward(self):
        # le deplacement ne se fait que si il n'ya pas de collisin avec un groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # si le monstre est en collisin avec le joueur
        else:
            # infliger des degats au joueur
            self.game.player.damage(self.attack)


# definir une classe de la momie
class Mummy(Monster):

    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(2)
        self.set_loot_amount(20)


# definir une classe de la l'alien
class Alien(Monster):

    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 130)
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(60)
