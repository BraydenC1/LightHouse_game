import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift, *args, **kwargs):
        if args:
            pass

        self.rect.x += x_shift
        self.rect.y += y_shift

