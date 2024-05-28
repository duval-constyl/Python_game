import pygame

# la classe qui  va gere le projectile
class Projectile(pygame.sprite.Sprite):

    #definir le constructeur de la classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 2
        self.image = pygame.image.load('Assets/projectile.png')
        self.player = player
        # reduire l'image du projectile
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # tourner le projectile
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        # supprimer le projectile apres qu'il soit lancé
        self.player.all_projectiles.remove(self)

    def pause_projectile(self):
        self.rect.x = 0
        self.angle = 0

    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        # verifier si le projectile entre en collision avec un monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            # supprimer le projectile
            self.remove()
            # infliger des degats
            monster.damage(self.player.attack)


        # verifier si notre projectile n'est plus present sur l'ecran
        if self.rect.x > 1080:
            self.remove()

