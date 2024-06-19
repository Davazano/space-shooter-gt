import pygame
from os.path import join
from random import randint

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

surf = pygame.Surface((100, 150))
surf.fill((0, 127, 127))

# player
path = join("space_shooter", "images", "player.png")
print(path)
player_surf = pygame.image.load(path).convert_alpha()
# player_rect = player_surf.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# star
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
star_position = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

# meteor
meteor_surf = pygame.image.load(join("space_shooter", "images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser
laser_surf = pygame.image.load(join("space_shooter", "images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

running = True
player_direction = 1

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill("darkgray")

    for pos in star_position:
        display_surface.blit(star_surf, pos)

    display_surface.blit(meteor_surf, meteor_rect)

    display_surface.blit(laser_surf, laser_rect)

    player_rect.x += 0.3 * player_direction
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_direction *= -1

    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()
quit()