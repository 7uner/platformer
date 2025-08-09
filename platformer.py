import math
from pathlib import Path

import pygame
import sys

pygame.init()

FPS = 60

# constants
WIDTH = 810
HEIGHT = 540
RED = (255, 0, 0)
background_absolute_width = 1200

# variables
player_x = WIDTH/2
player_y = HEIGHT - 137
scroll = 0
tiles = math.ceil(WIDTH / background_absolute_width) + 1

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Load background image
background = pygame.image.load(Path("images/background.png").resolve().as_posix())
background = pygame.transform.scale(background, (background_absolute_width, HEIGHT))
background_reverse = pygame.image.load(Path("images/background_reverse.png").resolve().as_posix())
background_reverse = pygame.transform.scale(background_reverse, (background_absolute_width, HEIGHT))

# set up game clock
clock = pygame.time.Clock()

# main loop
running = True
while running:
    # maintain game FPS
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 10
        # if the player is on the right half of the screen, then anymore movement
        # will push the background forward as well
        if player_x < WIDTH/3:
            scroll += 10
            player_x += 10
    if keys[pygame.K_RIGHT]:
        player_x += 10
        if player_x > WIDTH/3 * 2:
            scroll -= 10
            player_x -= 10
    # TODO: add a key press for the space bar, when pressed, allow the player_y to increase, at a certain height,
    # todo: start reducing their height, this creates a jumping effect
    if keys[pygame.K_SPACE]:
        pass

    # drawing
    screen.fill((0, 0, 0))

    i = -1
    while (i < tiles):
        print(background.get_width() * i + scroll, scroll)
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1
    pygame.draw.rect(screen, RED, (player_x, player_y, 30, 80))
    # RESET THE SCROLL FRAME
    if abs(scroll) > background.get_width():
        scroll = 0


    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
