import pygame
from support import import_folder

class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, size, image_path, is_wood_pile=True, animation_speed=5):
        super().__init__()
        self.is_wood_pile = is_wood_pile
        self.fire_images = import_folder('graphics/Map/fire/')  
        self.current_frame = 0
        self.animation_speed = animation_speed  
        self.animation_timer = 0

        self.image_path = image_path
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def transform_to_fire(self):
        self.is_wood_pile = False
        self.current_frame = 0

    def update(self, x_shift, y_shift, *args, **kwargs):
        
        if args:
           
            pass

        self.rect.x += x_shift
        self.rect.y += y_shift

        if not self.is_wood_pile:
            
            self.animation_timer += 1

            if self.animation_timer >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.fire_images)
                self.image = self.fire_images[self.current_frame]
                self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                self.animation_timer = 0  