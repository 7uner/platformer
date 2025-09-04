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
BLACK = (200, 200, 200)
background_absolute_width = 1200

# variables
player_x = WIDTH/2
player_y = HEIGHT - 137
player_y_speed = 0
max_jump_height = HEIGHT - 137 - 160
acceleration = 0
scroll = 0
# jumpstate 1: still 2: jumping up 3: jumping down 4: second jump
jump_state = 1
number_of_jumps = 2
tiles = math.ceil(WIDTH / background_absolute_width) + 1

# rectangles
player = pygame.Rect(WIDTH // 2, HEIGHT - 137, 30, 80)
platforms = [
    pygame.Rect(WIDTH / 2, HEIGHT / 2, 100, 30),
    pygame.Rect(WIDTH * 1.3, HEIGHT / 1.5, 100, 30),
    pygame.Rect(WIDTH * 2, HEIGHT / 2.2, 100, 30),
    pygame.Rect(WIDTH * 2.5, HEIGHT / 1.8, 100, 30),
]

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Load background image
background = pygame.image.load(Path("images/background.png").resolve().as_posix())
background = pygame.transform.scale(background, (background_absolute_width, HEIGHT))

# set up game clock
clock = pygame.time.Clock()

def handleInput():
    global player_x, scroll, jump_state, number_of_jumps, player_y_speed, acceleration, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 10
        # if the player is on the right half of the screen, then anymore movement
        # will push the background forward as well
        if player.x < WIDTH/3:
            scroll += 10
            player.x += 10
            for platform in platforms:
                platform.x += 10
    if keys[pygame.K_RIGHT]:
        player.x += 10
        if player.x > WIDTH/3 * 2:
            scroll -= 10
            player.x -= 10
            for platform in platforms:
                platform.x -= 10

    if keys[pygame.K_SPACE]:
        if jump_state == 1 and number_of_jumps > 0:
            player_y_speed = -10
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1
        elif (jump_state == 3) and number_of_jumps > 0:
            player_y_speed = -10
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1


def update():
    global jump_state, player, player_y_speed, acceleration, number_of_jumps
    if jump_state == 2 and player_y_speed >= 0:
        player_y_speed = 0
        acceleration = 0.3
        jump_state = 3
    # if the player hits the ground, set speed back to 0
    if player.y > HEIGHT - 137:
        player.y = HEIGHT - 137
        player_y_speed = 0
        acceleration = 0
        jump_state = 1
        number_of_jumps = 2
    # constantly update the speed
    player_y_speed += acceleration
    player.y += player_y_speed


def draw():
    global scroll
    # drawing
    screen.fill((0, 0, 0))

    i = -1
    while i < tiles:
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1
    pygame.draw.rect(screen, RED, player)
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)
    # RESET THE SCROLL FRAME
    if abs(scroll) > background.get_width():
        scroll = 0

    # Update display
    pygame.display.flip()

# main loop
running = True
while running:
    # maintain game FPS
    clock.tick(FPS)
    handleInput()
    update()
    draw()


pygame.quit()
sys.exit()
