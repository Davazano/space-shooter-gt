import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join("space_shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            # print(current_time)
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])   
        # # we use normalization to ensure that the player direction is not greater than 1 for example when player moves up and down at the same time
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        # print((self.direction * self.speed).magnitude())
        # print(self.direction)

        # fire laser
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, group, surf):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        # Destroy laser if it goes off screen
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        # self.spawned_time = pygame.time.get_ticks()
        # self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(100, 500)
    
    def update(self, dt):
        # Move meteor
        self.rect.center += self.direction * self.speed * dt

        # Destroy meteor after 2 seconds
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
            print("Meteor destroyed")
        # current_time = pygame.time.get_ticks()
        # if current_time - self.spawned_time >= self.lifetime:
        #     self.kill()

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# import
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("space_shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("space_shooter", "images", "laser.png")).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()
# star sprites
for pos in range(20):
    Star(all_sprites, star_surf)
# player sprite
player = Player(all_sprites)

# Custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

running = True

while running:
    # if you don't pass parameters into clock.tick() then your computer will decide the frame rate
    dt = clock.tick() / 1000 #delta time in per seconds
    # print(clock.get_fps())

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)

    all_sprites.update(dt)

    # draw the game
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
quit()