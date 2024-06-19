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
x = 50
y = 100

# star
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
star_position = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

running = True

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill("darkgray")

    x += 0.1
    display_surface.blit(player_surf, (x, y))

    for pos in star_position:
        display_surface.blit(star_surf, pos)
    pygame.display.update()

pygame.quit()
quit()