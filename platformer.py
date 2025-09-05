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
deltaY = 0
deltaX = 0
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
    global player_x, scroll, jump_state, number_of_jumps, deltaY, acceleration, running, deltaX
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        deltaX = -10

    if keys[pygame.K_RIGHT]:
        deltaX = 10

    if keys[pygame.K_SPACE]:
        if jump_state == 1 and number_of_jumps > 0:
            deltaY = -10
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1
        elif (jump_state == 3) and number_of_jumps > 0:
            deltaY = -10
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1


def handleYCollision():
    global platforms, player, deltaY, jump_state, number_of_jumps
    for platform in platforms:
        if player.colliderect(platform):
            # falling down on to a platform
            if deltaY > 0 and player.bottom <= platform.bottom:
                player.bottom = platform.top
                deltaY = 0
                jump_state = 1
                number_of_jumps = 2
            # hitting underside of a platform
            elif deltaY < 0:
                player.top = platform.bottom
                deltaY = 3


def handleXCollision():
    global platforms, player, deltaY, jump_state, number_of_jumps
    for platform in platforms:
        if player.colliderect(platform):
            # hitting left side of a platform
            if deltaX > 0:
                player.right = platform.left
            # hitting right side of a platform
            elif deltaX < 0:
                player.left = platform.right


def update():
    global jump_state, player, deltaY, acceleration, number_of_jumps, scroll, deltaX
    # update jumps
    if jump_state == 2 and deltaY >= 0:
        deltaY = 0
        acceleration = 0.3
        jump_state = 3
    # if the player hits the ground, set speed back to 0
    if player.y > HEIGHT - 137:
        player.y = HEIGHT - 137
        deltaY = 0
        acceleration = 0
        jump_state = 1
        number_of_jumps = 2
    # constantly update the speed
    player.x += deltaX
    # if the player is on the right half of the screen, then anymore movement
    # will push the background forward as well
    if player.x < WIDTH / 3:
        scroll -= deltaX
        player.x -= deltaX
        for platform in platforms:
            platform.x -= deltaX
    elif player.x > WIDTH/3 * 2:
        scroll -= deltaX
        player.x -= deltaX
        for platform in platforms:
            platform.x -= deltaX
    handleXCollision()
    
    deltaY += acceleration
    player.y += deltaY
    handleYCollision()
    deltaX = 0


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
