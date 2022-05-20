import random
from turtle import update
from typing import Counter
import pygame
import sprites
from sprites import *
pygame.init()

from pygame.locals import (

    K_UP,

    K_DOWN,

    K_LEFT,

    K_RIGHT,

    K_ESCAPE,

    KEYDOWN,

    QUIT,

)


            

LIVES=20

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

LASER_OFFSET = 12

PAUSE_SIZE = (200,200)

pygame.display.set_icon(pygame.transform.scale(pygame.image.load('Icon.png'), (32,32)))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Star Wars!')




player = sprites.Player((SCREEN_WIDTH + 25)/2 ,SCREEN_HEIGHT - 55/4)
laser = Laser(LASER_OFFSET, 1)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
running = True
laser_width = 1
targets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
paused = False
counter = Counter(LIVES)
all_sprites.add(counter)
done = False

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            if event.button == 1:
                laser.fire(player, screen, targets, .25, all_sprites, counter, done)
            elif event.button == 2:
                foo = Nuke(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], .25)
                all_sprites.add(foo)
                targets.add(foo)
    done = draw(paused, screen, all_sprites, targets, laser, player, counter, done)


