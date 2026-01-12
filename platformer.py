import math
import random
from pathlib import Path
import pygame
import sys

pygame.init()

FPS = 60

# constants
WIDTH = 850
HEIGHT = 540
RED = (255, 0, 0)
BLACK = (200, 200, 200)
background_absolute_width = 1200
floor_height = 80

# variables
player_speed = 7
jump_speed = 10
deltaY = 0
deltaX = 0
acceleration = 0
scroll = 0
direction = "right"
# jumpstate 1: still 2: jumping up 3: jumping down 4: second jump
jump_state = 1
number_of_jumps = 2
tiles = math.ceil(WIDTH / background_absolute_width) + 1

# player
player = pygame.Rect(WIDTH // 4 + 75, HEIGHT // 2 - 80, 60, 80)
player_run_left_sprite = pygame.image.load(Path("images/pika_run_left_2x.png").resolve().as_posix())
player_run_right_sprite = pygame.transform.flip(player_run_left_sprite, True, False)
player_jump_left_sprite = pygame.image.load(Path("images/pika_jump_left.PNG").resolve().as_posix())
player_jump_right_sprite = pygame.transform.flip(player_jump_left_sprite, True, False)


pika_run_frame = 0
pika_run_tick = 0
pika_run_left_frames = []
pika_run_right_frames = []
pika_size = player_run_left_sprite.get_width()/5
for i in range(5):
    frame = player_run_left_sprite.subsurface(i * pika_size, 0, pika_size, player_run_left_sprite.get_height())
    pika_run_left_frames.append(frame)
for i in range(4, -1, -1):
    frame = player_run_right_sprite.subsurface(i * pika_size, 0, pika_size, player_run_right_sprite.get_height())
    pika_run_right_frames.append(frame)

pika_jump_frame = 0
pika_jump_tick = 0
pika_jump_left_frames = []
pika_jump_right_frames = []
pika_size = player_jump_right_sprite.get_width()/21
for i in range(21):
    frame = player_jump_left_sprite.subsurface(i * pika_size, 0, pika_size, player_jump_left_sprite.get_height())
    pika_jump_left_frames.append(frame)
for i in range(20, -1, -1):
    frame = player_jump_right_sprite.subsurface(i * pika_size, 0, pika_size, player_jump_right_sprite.get_height())
    pika_jump_right_frames.append(frame)

# platforms
PLATFORM_MIN_WIDTH = 3
PLATFORM_MAX_WIDTH = 7
PLATFORM_HEIGHT = 30
PLATFORM_GAP_Y = 120
platforms = [pygame.Rect(WIDTH // 4, HEIGHT // 2, 150, PLATFORM_HEIGHT)]

# coins
coins_collected = 0
coins = []
COIN_SIZE = 50
COIN_FRAMES = 8
coin_spritesheet = pygame.image.load(Path("images/coin_gold.png").resolve().as_posix())
coin_spritesheet = pygame.transform.scale(coin_spritesheet, (COIN_FRAMES * COIN_SIZE, COIN_SIZE))
coin_frames = []
for i in range(COIN_FRAMES):
    frame = coin_spritesheet.subsurface(i * COIN_SIZE, 0, COIN_SIZE, COIN_SIZE).copy()
    coin_frames.append(frame)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Load background image
background = pygame.image.load(Path("images/BG2.png").resolve().as_posix())
background = pygame.transform.scale(background, (background_absolute_width, HEIGHT))
# load platform sprite
platform_sprite = pygame.image.load(Path("images/tiles_spritesheet.png").resolve().as_posix())
# extract sub surfaces that we need
grass = platform_sprite.subsurface((648, 0, 70, 70))
grass = pygame.transform.scale(grass, (PLATFORM_HEIGHT, PLATFORM_HEIGHT))
# set up game clock
clock = pygame.time.Clock()

# hud variables
coin_hud_frame = 0
coin_hud_tick = 0


def handleInput():
    global scroll, jump_state, number_of_jumps, deltaY, acceleration, running, deltaX, direction, pika_jump_tick, \
        pika_jump_frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        deltaX = -player_speed
        direction = "left"

    if keys[pygame.K_d]:
        deltaX = player_speed
        direction = "right"

    if keys[pygame.K_SPACE]:
        if jump_state == 1 and number_of_jumps > 0:
            deltaY = -jump_speed
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1
            pika_jump_tick = 0
            pika_jump_frame = 0
        elif (jump_state == 3) and number_of_jumps > 0:
            deltaY = -jump_speed
            acceleration = 0.3
            jump_state = 2
            number_of_jumps -= 1
            pika_jump_tick = 0
            pika_jump_frame = 0


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


def handle_item_collision():
    global coins_collected, coins
    new_coins = []
    for coin in coins:
        if player.colliderect(coin["rect"]):
            coins_collected += 1
            print(f"You have {coins_collected} coins!")
        else:
            new_coins.append(coin)
    coins = new_coins
    # item collision should be handled separately, we will use another series of if condition, to see which item
    # we collided with, and perform the appropriate action to the item


def update():
    global jump_state, player, deltaY, acceleration, number_of_jumps, scroll, deltaX, platforms, coins
    # update jumps
    if jump_state == 2 and deltaY >= 0:
        deltaY = 0
        acceleration = 0.3
        jump_state = 3
    # if the player hits the ground, set speed back to 0
    if player.y > HEIGHT - floor_height:
        player.y = HEIGHT - floor_height
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
        for coin in coins:
            coin["rect"].x -= deltaX
    elif player.x > WIDTH/3 * 2:
        scroll -= deltaX
        player.x -= deltaX
        for platform in platforms:
            platform.x -= deltaX
        for coin in coins:
            coin["rect"].x -= deltaX

    # based on the scroll value, remove old platforms that's now off screen, add new
    # platforms to forward screen
    if platforms[-1].x - scroll < 2 * WIDTH:
        platforms.extend(generate_platforms(platforms[-1].x + 200, 5))

    # advance coin animation & bobbing timing
    for c in coins:
        # advance frame every N ticks (controls animation speed)
        c["tick"] += 1
        if c["tick"] >= 6:  # tweak this for faster/slower animation
            c["tick"] = 0
            c["frame"] = (c["frame"] + 1) % COIN_FRAMES

    platforms = [p for p in platforms if p.right > scroll - 200]
    coins = [c for c in coins if c["rect"].right > scroll - 200]

    handleXCollision()
    deltaY += acceleration
    player.y += deltaY
    handleYCollision()
    handle_item_collision()

    deltaX = 0


def draw():
    global scroll, coin_hud_frame, coin_hud_tick, pika_run_tick, pika_run_frame, direction, pika_jump_tick, \
        pika_jump_frame
    # drawing
    screen.fill((0, 0, 0))

    i = -1
    while i < tiles:
        screen.blit(background, (background.get_width() * i + scroll, 0))
        i += 1
    # draw the player animation if running
    # pygame.draw.rect(screen, RED, player)
    if direction == "right" and jump_state != 2 and jump_state != 3:
        screen.blit(pika_run_right_frames[pika_run_frame], (player.x - 30, player.y))
    if direction == "left" and jump_state != 2 and jump_state != 3:
        screen.blit(pika_run_left_frames[pika_run_frame], (player.x, player.y))
    # jumping animation
    if direction == "right" and jump_state == 2 or direction == "right" and jump_state == 3:
        screen.blit(pika_jump_right_frames[pika_jump_frame], (player.x, player.y - 50))
    if direction == "left" and jump_state == 2 or direction == "left" and jump_state == 3:
        screen.blit(pika_jump_left_frames[pika_jump_frame], (player.x, player.y - 50))
    # update player animation frames
    pika_run_tick += 1
    if pika_run_tick >= 6:
        pika_run_frame += 1
        pika_run_tick = 0
    if pika_run_frame >= 4:
        pika_run_frame = 0

    if jump_state == 2 or jump_state == 3:
        pika_jump_tick += 1
        if pika_jump_tick >= 4:
            pika_jump_frame += 1
            pika_jump_tick = 0
        if pika_jump_frame >= 20:
            pika_jump_frame = 0

    for platform in platforms:
        n = platform.width // 30
        for i in range(n):
            screen.blit(grass, (platform.x + i * 30, platform.y))

    # draw the coins with animation
    for c in coins:
        rect = c["rect"]
        # bobbing offset (vertical) using sine wave
        bob = int(math.sin(pygame.time.get_ticks() / 300 + c["phase"]) * 6)  # amplitude = 6 px
        # get current frame surface
        frame_surf = coin_frames[c["frame"]]
        # world -> screen coords by applying scroll
        screen_x = rect.x
        screen_y = rect.y + bob
        # blit coin (center aligned)
        screen.blit(frame_surf, (screen_x, screen_y))

    # RESET THE SCROLL FRAME
    if abs(scroll) > background.get_width():
        scroll = 0

    # hud elements
    # fonts
    font = pygame.font.Font(None, 50)
    # text surfaces
    coin_hud = font.render(f"X{coins_collected}", True, (200, 50, 50))
    text_rect = coin_hud.get_rect()
    text_rect.x = 50
    text_rect.y = 10
    screen.blit(coin_hud, text_rect)
    screen.blit(coin_frames[coin_hud_frame], (0, 0))
    coin_hud_tick += 1
    if coin_hud_tick >= 6:
        coin_hud_frame += 1
        coin_hud_tick = 0
    if coin_hud_frame >= 8:
        coin_hud_frame = 1

    # Update display
    pygame.display.flip()


def generate_platforms(start_x=WIDTH/2+100, num=8):
    platforms = []
    x = start_x
    for i in range(num):
        width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH) * 30
        y = random.randint(200, HEIGHT - floor_height)
        platforms.append(pygame.Rect(x, y, width, PLATFORM_HEIGHT))
        generate_coins(x, y, width)
        x += width + random.randint(250, 500)
    return platforms


def generate_coins(plat_x, plat_y, plat_width):
    chance = random.randint(1, 1)
    if chance == 1:
        coin_x = plat_x + random.randint(5, plat_width - COIN_SIZE)
        coin_y = plat_y - COIN_SIZE - 10
        frame_idx = random.randint(0, COIN_FRAMES - 1)  # start on a random frame
        phase = random.random() * 2 * math.pi  # unique phase so coins don't bob identically
        coins.append({"rect": pygame.Rect(coin_x, coin_y, COIN_SIZE, COIN_SIZE),
                      "frame": frame_idx,
                      "phase": phase,
                      "tick": 0})  # tick used to advance frame timing


def add_items():
    items = []
    # for each item, we will loop though it, and use a series of if conditions, to check what kind of
    # item it is. Then we can add that item in to the space.

# main loop
running = True
platforms.extend(generate_platforms(num=8))

while running:
    # maintain game FPS
    clock.tick(FPS)
    handleInput()
    update()
    draw()


pygame.quit()
sys.exit()
