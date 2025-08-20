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
# jump state 1: still 2: jumping up 3: jumping down 4: second jump
jump_state = 1
number_of_jumps = 2
tiles = math.ceil(WIDTH / background_absolute_width) + 1

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Load background image
background = pygame.image.load(Path("images/background.png").resolve().as_posix())
background = pygame.transform.scale(background, (background_absolute_width, HEIGHT))

# rectangles
player_rect = pygame.Rect(player_x, player_y, 30, 80)
platform = pygame.Rect(WIDTH/2, HEIGHT/2, 100, 50)

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

    if platform.top <= player_rect.bottom <= platform.bottom and player_rect.right > platform.left and player_rect.left < platform.right:
        player_y_speed = 0
        acceleration = 0
        number_of_jumps = 2
        jump_state = 1
    # if we are currently standing on the platform and slide left or right, we should start dropping
    if (player_rect.right < platform.left or player_rect.left > platform.right) and jump_state == 1 and player_rect.y < HEIGHT - 137:
        acceleration = 0.3
        number_of_jumps = 0
        jump_state = 3
        print("SHOULD BE FALLING")
    # if the player head jumps into a platform
    if platform.top <= player_rect.top <= platform.bottom and player_rect.right > platform.left and player_rect.left < platform.right:
        player_y_speed = 3
        acceleration = 0.3
        number_of_jumps = 0
        jump_state = 3
        print("OUCH MY HEAD")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not (player_rect.left == platform.right and player_rect.top < platform.bottom and player_rect.bottom > platform.top):
            player_rect.x -= 10
            # if the player is on the right half of the screen, then anymore movement
            # will push the background forward as well
            if player_rect.x < WIDTH/3:
                scroll += 10
                player_rect.x += 10
    if keys[pygame.K_RIGHT]:
        if not (player_rect.right == platform.left and player_rect.top < platform.bottom and player_rect.bottom > platform.top):
            player_rect.x += 10
            if player_rect.x > WIDTH/3 * 2:
                scroll -= 10
                player_rect.x -= 10
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

    # handle loop events


    # handle jump acceleration
    # if player hits max jump height, make him start falling down
    if jump_state == 2 and player_y_speed >= 0:
        player_y_speed = 0
        acceleration = 0.3
        jump_state = 3
    # if the player hits the ground, set speed back to 0
    if player_rect.y > HEIGHT - 137:
        player_rect.y = HEIGHT - 137
        player_y_speed = 0
        acceleration = 0
        jump_state = 1
        number_of_jumps = 2
    # constantly update the speed
    player_y_speed += acceleration
    player_rect.y += player_y_speed

    # drawing
    screen.fill((0, 0, 0))

    i = -1
    while i < tiles:
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1
    pygame.draw.rect(screen, RED, (player_rect.x, player_rect.y, 30, 80))

    pygame.draw.rect(screen, BLACK, platform)
    # RESET THE SCROLL FRAME
    if abs(scroll) > background.get_width():
        scroll = 0

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
