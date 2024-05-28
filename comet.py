import  pygame
import random

# creer une classe pour gerer les comet
class Comet(pygame.sprite.Sprite):

    def __init__(self, comet_event):
        super().__init__()
        self.image = pygame.image.load('Assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 3)
        self.rect.x = random.randint(20, 800)
        self.rect.y = - random.randint(0, 800)
        self.comet_event = comet_event

    def remove(self):
        self.comet_event.all_comets.remove(self)
        # joueur le son
        self.comet_event.game.sound_manager.play('meteorite')

        # verifier si le omre de comets est à 0
        if len(self.comet_event.all_comets) == 0:
            # remettre la barre à 0
            self.comet_event.reset_percent()

            # apparaittre les 2 monstre
            self.comet_event.game.start()

    def fall(self):
        self.rect.y += self.velocity

        # ne tombe pas sur le sol
        if self.rect.y >= 500:
            print("sol")
            # retirer la boue de feu
            self.remove()

            # s'il n'ya plus de boule de feu
            if len(self.comet_event.all_comets) == 0:
                print("L'evenement est fini")
                # remettre la jauge au depart
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False

        # verifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print("joueur touché")
            # retirer la boule de feu
            self.remove()
            # subir 10 points de degats
            self.comet_event.game.player.damage(10)
