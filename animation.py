import pygame


# definir une classe qui va s'occuper des animations
class AnimateSprite(pygame.sprite.Sprite):

    # definir les choses à faire à la creatin de l'entite
    def __init__(self, sprite_name, size=(200, 200)):
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f'Assets/{sprite_name}.png')
        self.current_image = 0 # commencer l'anim à l'image 0
        self.images = animation.get(sprite_name)
        self.animation = False

    # definir une methode pour enclencher l'animation
    def start_animation(self):
        self.animation = True

    # definir une methode pour animer le sprite
    def animate(self, loop=False):

        # verifier si l'animation est active
        if self.animation:
            # passer a l'image suivant
            self.current_image += 1

            # verifier si on a atteint la fin de l'animation
            if self.current_image >= len(self.images):
                # remettre l'animation au depart
                self.current_image = 0

                # verifier si l'animation n'est pas en mode boucle
                if loop is False:
                    # desactiver l'animation
                    self.animation = False

            # modifier l'image precedente par la suivante
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)


# definir une fonction pour charger les images d'un sprite
def load_animation_images(sprite_name):
    # charger les 24 images de ce sprite dans le dossier corresponant
    images = []
    # recuperer le chemin du dossier pour ce sprite
    path = f"Assets/{sprite_name}/{sprite_name}"

    # boucle sur chaque image du dossier
    for num in range(1, 24):
        image_path = path + str(num) + '.png'
        images.append(pygame.image.load(image_path))

    # renvoyer le contenu
    return images


# definir un dictionnaire qui va contenir les images chargées de chacun
animation = {
    'mummy': load_animation_images('mummy'),
    'player': load_animation_images('player'),
    'alien': load_animation_images('alien')
}
