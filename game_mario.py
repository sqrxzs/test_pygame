import pygame
import os
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Корпоративный мессенджер - Игровая сцена")

clock = pygame.time.Clock()

# Загрузка изображений
def load_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
        images.append(img)
    return images

player_run = load_images("assets/player")
enemy_run = load_images("assets/enemy")
jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8

    def update(self, keys):
        self.image_index += 0.1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

        self.direction.x = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_power
            self.on_ground = False
            jump_sound.play()

        self.direction.y += self.gravity
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True

player = Character(100, HEIGHT - 150, player_run)
enemy = Character(600, HEIGHT - 150, enemy_run)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

# Игровой цикл
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(keys)

    screen.fill((100, 150, 255))  # фон
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
