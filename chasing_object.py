import pygame
from support import import_folder

class ChasingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, animation_speed=5):
        super().__init__()

        self.chasing_images = import_folder('graphics/Map/wave/')  
        self.current_frame = 0
        self.animation_speed = animation_speed  
        self.animation_timer = 0

        self.image = self.chasing_images[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self, world_shift):
        self.rect.x += self.speed
        self.rect.x += world_shift

        
        self.animation_timer += 1

        
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.chasing_images)
            self.image = self.chasing_images[self.current_frame]
            self.animation_timer = 0  