import pygame, sys
from tiles import Tile
from settings import tile_size, screen_width, screen_height, level_map
from player import Player
from background import Background
from chasing_object import ChasingObject
from fire import Fire
from time import sleep, time
import threading


class Level:
    def __init__(self, level_data, surface, background_images):
        # level setup
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.world_shift = 0
        self.vertical_shift = 0
        self.setup_level(level_data)
        self.level_width = len(level_data[0]) * tile_size
        self.background = Background(background_images)
        self.chasing_objects = pygame.sprite.Group()
        self.create_chasing_object()
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.show_win_screen_after_delay = False
        self.delayed_win_screen_start_time = 0

    def create_chasing_object(self):
        chasing_object = ChasingObject(-1500, 100, 4)  
        self.chasing_objects.add(chasing_object)
        
    def setup_level(self, layout):
        

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'Z':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/1.png')
                    self.tiles.add(tile)
                elif cell == 'X':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/2.png')
                    self.tiles.add(tile)
                elif cell == 'C':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/3.png')
                    self.tiles.add(tile)
                elif cell == 'V':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/4.png')
                    self.tiles.add(tile)
                elif cell == 'B':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/5.png')
                    self.tiles.add(tile)
                elif cell == 'N':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/6.png')
                    self.tiles.add(tile)
                elif cell == 'M':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/7.png')
                    self.tiles.add(tile)
                elif cell == 'L':
                    tile = Tile((x, y), tile_size, image_path='graphics/Map/blocks/8.png')
                    self.tiles.add(tile)

                elif cell == 'P':
                    player_sprite = Player((x, y + self.vertical_shift))
                    self.player.add(player_sprite)
                elif cell == 'F':
                    fire = Fire((x,y), tile_size, image_path='graphics/Map/wood/1.png')
                    self.tiles.add(fire)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if isinstance(sprite, Fire):
                continue  

            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True

        if player.on_left and (player.rect.left < sprite.rect.right or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > sprite.rect.left or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if isinstance(sprite, Fire):
                continue  

            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_collision_with_wood_pile(self):
        player = self.player.sprite
        wood_piles = [sprite for sprite in self.tiles.sprites() if isinstance(sprite, Fire) and sprite.is_wood_pile]
        
        for wood_pile in wood_piles:
            if player.rect.colliderect(wood_pile.rect):
                print("Player collided with wood pile!")
                wood_pile.transform_to_fire()

                
                 # Set a flag to indicate the win screen should be shown after 2 seconds
                self.show_win_screen_after_delay = True
                self.delayed_win_screen_start_time = pygame.time.get_ticks()
    
    def update_win_screen_after_delay(self):
        # Check if it's been 2 seconds since the wood pile interaction
        current_time = pygame.time.get_ticks()
        if self.show_win_screen_after_delay and current_time - self.delayed_win_screen_start_time >= 2000:
            self.show_win_screen()
            self.show_win_screen_after_delay = False
                
                


############  GAME OVER AND RESET  ################
    def reset(self):
        self.player.sprite.rect.topleft = (0, 0)
        self.player.sprite.direction = pygame.math.Vector2(0, 0)
        self.player.sprite.speed = 8
        self.player.sprite.on_ground = False
        self.player.sprite.on_ceiling = False
        self.player.sprite.on_left = False
        self.player.sprite.on_right = False

        # Reset x-scroll
        self.world_shift = 0

        # Reset chasing object
        self.chasing_objects.empty()
        self.create_chasing_object()

        # Clear existing tiles
        self.tiles.empty()

        # Clear existing tiles and recreate the level
        self.setup_level(level_map)

        # Reset other game state variables as needed
        self.game_over = False

    def check_collision_with_player(self):
        player = self.player.sprite
        collisions = pygame.sprite.spritecollide(player, self.chasing_objects, False )

        if collisions:
            print("Collision detected!")
            self.show_game_over_screen()

    def show_game_over_screen(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.display_surface.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to play again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        self.display_surface.blit(restart_text, restart_rect)

        pygame.display.flip()

        self.handle_game_over_input()

    def show_win_screen(self):
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.display_surface.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to play again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        self.display_surface.blit(restart_text, restart_rect)

        pygame.display.flip()

        self.handle_game_over_input()

    def handle_game_over_input(self):
        # Wait for the player to press 'R' to restart or 'Q' to quit
        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        waiting_for_input = False
                        return  
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    


    def run(self):

            # Background
            self.background.draw(self.display_surface)
            self.background.update()

            # level tiles
            self.tiles.update(self.world_shift, self.vertical_shift)
            self.tiles.draw(self.display_surface)
            self.scroll_x()

            # Chasing objects
            self.chasing_objects.update(self.world_shift)
            self.chasing_objects.draw(self.display_surface)

            # Check for collision with the player
            self.check_collision_with_player()

            # player
            self.player.update()
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.player.draw(self.display_surface)

            
            # Check for collision with the wood pile
            self.check_collision_with_wood_pile()
            
            # Update the win screen after delay if needed
            self.update_win_screen_after_delay()

            # Update display
            pygame.display.flip()
            
            #pygame.display.update()
            self.clock.tick(60)
            
        
