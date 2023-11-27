import pygame, sys
from settings import *
from level import Level

#basic setup for Pygame Window
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()


background_images = ['graphics/Map/background/1.png']
level = Level(level_map, screen, background_images)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                level.reset()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        

    
    screen.fill('black')
    level.run()
    pygame.display.update()
    