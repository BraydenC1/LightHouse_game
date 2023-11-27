import pygame

class Background:
    def __init__(self, image_paths):
        self.images = [pygame.image.load(path).convert() for path in image_paths]
        self.index = 0
        self.rect = self.images[self.index].get_rect()

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0

    def draw(self, surface):
        surface.blit(self.images[self.index], self.rect)