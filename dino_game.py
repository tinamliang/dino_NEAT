import pygame
import neat
import time
import math
import os
import random

WIN_WIDTH = 800
WIN_HEIGHT = 400

DINO_IMGS = [
    pygame.transform.scale(pygame.image.load(os.path.join("sprites", "dino_1.png")),  (60, 90)),
    pygame.transform.scale(pygame.image.load(os.path.join("sprites", "dino_3.png")),  (60, 90)),
    pygame.transform.scale(pygame.image.load(os.path.join("sprites", "dino_4.png")),  (60, 90))
]
CACTUS_IMG = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "cacti_large_1.png")), (30, 60))
DINO_DEAD = pygame.transform.scale(pygame.image.load(os.path.join("sprites", "dino_5.png")), (60, 90))

white = (255, 255, 255)
grey = (211, 211, 211)

score = 0
player_x = 50
player_y = 215

obstacle_x = 250
obstacle_y = 250
gravity = 1
speed = 3

game_over = False

background = white

pygame.init()
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
bg = pygame.image.load("sprites/ground.png").convert_alpha()
bg_width = bg.get_width()

scroll = 0
tiles = math.ceil(WIN_WIDTH / bg_width) + 1


class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_change = 0
        self.index = 0
        self.count = 0
        self.img = DINO_IMGS[self.index]

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def jump(self):
        if self.y_change > 0 or self.y < 215:
            self.y -= self.y_change
            self.y_change -= gravity
        if self.y > 215:
            self.y = 215
        if self.y == 215 and self.y_change < 0:
            self.y_change = 0

    def update(self):
        self.count += 1
        if self.index == len(DINO_IMGS):
            self.index = 0
        self.img = DINO_IMGS[self.index]
        if self.count > 5: # to slow down dino's little legs
            self.index += 1
            self.count = 0


class Obstacle:
    def __init__(self, y):
        self.x = [400, 1000, 1400]
        self.y = y
        self.img = CACTUS_IMG

    def draw(self, window, x_index):
        window.blit(self.img, (x_index, self.y))

    def collide(self, dino, x_index):
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)
        offset = (x_index - dino.x, self.y - round(dino.y))

        b_point = dino_mask.overlap(cactus_mask, offset)

        if b_point:
            return True
        return False


fps = 60 # frame rate
running = True
dino = Dino(player_x, player_y)
cactus = Obstacle(obstacle_y)

while running:

    if game_over:
        dino.img = DINO_DEAD
        dino.draw(screen)
        scroll = 0
        speed = 0

    timer.tick(fps)  # control speed at which it runs
    screen.fill(background)

    # infinite moving background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 296))

    scroll -= 3
    if abs(scroll) > bg_width:
        scroll = 0

    for i in range(len(cactus.x)):
        cactus.x[i] -= speed
        if cactus.x[i] < -30:
            cactus.x.remove(cactus.x[i])
            cactus.x.append(random.randint(cactus.x[-1] + 280, cactus.x[-1] + 320))
        cactus.draw(screen, cactus.x[i])

        if cactus.collide(dino, cactus.x[i]):
            game_over = True

    dino.jump()
    dino.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dino.y_change == 0:
                dino.y_change = 18

    dino.update()
    pygame.display.flip()
pygame.quit()

