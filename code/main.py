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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
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
        # Move laser up
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


def collisions():
    global running
    # check for collision between player and meteor
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        running = False
        print(collision_sprites[0])

    # check for collision between laser and meteor
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            print(collided_sprites[0])

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 10).move(0, -8), 5, 10)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# import
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("space_shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("space_shooter", "images", "laser.png")).convert_alpha()
font = pygame.font.Font(join("space_shooter", 'images', 'Oxanium-Bold.ttf'), 40)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
# star sprites
for pos in range(20):
    Star(all_sprites, star_surf)
# player sprite
player = Player(all_sprites)

# Custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

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
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    all_sprites.update(dt)
    collisions()

    # draw the game
    display_surface.fill('#3a2e3f') 
    display_score()
    all_sprites.draw(display_surface)

    # draw test
    # pygame.draw.rect(display_surface, 'red', player.rect, 10, 10)

    pygame.display.update()

pygame.quit()
quit()