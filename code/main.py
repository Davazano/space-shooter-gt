import pygame
from os.path import join
from random import randint

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

surf = pygame.Surface((100, 150))
surf.fill((0, 127, 127))

# player
path = join("space_shooter", "images", "player.png")
print(path)
player_surf = pygame.image.load(path).convert_alpha()
# player_rect = player_surf.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2()
player_speed = 300

# star
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
star_position = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

# meteor
meteor_surf = pygame.image.load(join("space_shooter", "images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser
laser_surf = pygame.image.load(join("space_shooter", "images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))


# rect
# plain_rect = pygame.FRect(left, top, width, height)

running = True

while running:
    # if you don't pass parameters into clock.tick() then your computer will decide the frame rate
    dt = clock.tick() / 1000 #delta time in per seconds
    # print(clock.get_fps())

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
    
    # input
    # print(pygame.mouse.get_rel())
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])   
    # we use normalization to ensure that the player direction is not greater than 1 for example when player moves up and down at the same time
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rect.center += player_direction * player_speed * dt
    # print((player_direction * player_speed).magnitude())
    # print(player_direction)

    # fire laser
    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
        print("fire laser")

    # draw the game
    display_surface.fill("darkgray")

    for pos in star_position:
        display_surface.blit(star_surf, pos)

    display_surface.blit(meteor_surf, meteor_rect)

    display_surface.blit(laser_surf, laser_rect)

    # Player Movement
    # if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
    #     player_direction.y *= -1
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction.x *= -1

    # player_rect.center += player_direction * player_speed * dt

    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction *= -1

    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()
quit()