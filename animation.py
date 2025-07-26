from pathlib import Path

import pygame
import sys

pygame.init()

# Create window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Blit Example")

# Load image
sprite_sheet = pygame.image.load(Path("../../projects/images/nyan_cat.png").resolve().as_posix())

#TODO:based on the new sprite size and loation, change the width and height appropriately
frame_width = 150
frame_height = 100
#TODO: we need to calculate this y location based on where the top left corner of the sprite section is
sprite_y_location = 0
frames = []
for i in range(6):
    frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, sprite_y_location, frame_width, frame_height))
    frames.append(frame)

current_frame = 0
animation_speed = 0.1 # controls how fast the animation changes
frame_timer = 0
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000  # delta time in secondsw
    # Update frame timer
    frame_timer += dt
    if frame_timer >= animation_speed:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(frames)

    # Fill screen with white color before bliting
    screen.fill((255, 255, 255))

    # Blit image at (100, 150)
    screen.blit(frames[current_frame], (150, 100))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
