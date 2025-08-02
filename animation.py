from pathlib import Path

import pygame
import sys

pygame.init()

# Create window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Blit Example")

# Load image
sprite_sheet = pygame.image.load(Path("images/nyan_cat.png").resolve().as_posix())

# sprite dimensions
title_screen_frame_width = 150
title_screen_frame_height = 100
rocket_frame_width = 116.5
rocket_frame_height = 50
super_cat_width = 80
super_cat_height = 40

title_screen_sprite_y_location = 0
rocket_sprite_y_location = 265
super_cat_y_location = 220
title_screen_frames = []
rocket_frames = []
super_frames = []

for i in range(6):
    frame = sprite_sheet.subsurface(pygame.Rect(i * title_screen_frame_width, title_screen_sprite_y_location,
                                                title_screen_frame_width, title_screen_frame_height))
    title_screen_frames.append(frame)

for i in range(4):
    print(i * rocket_frame_width, rocket_sprite_y_location,
                                                rocket_frame_width, rocket_frame_height)
    frame = sprite_sheet.subsurface(pygame.Rect(i * rocket_frame_width, rocket_sprite_y_location,
                                                rocket_frame_width, rocket_frame_height))
    rocket_frames.append(frame)
for i in range(4):
    print(i * super_cat_width, super_cat_y_location,
                                                super_cat_width, super_cat_height)
    frame = sprite_sheet.subsurface(pygame.Rect(i * super_cat_width,super_cat_y_location,
                                                super_cat_width, super_cat_height))
    super_frames.append(frame)
title_screen_current_frame = 0
rocket_current_frame = 0
super_current_frame = 0
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
        #progress each sprite by 1 frame
        title_screen_current_frame = (title_screen_current_frame + 1) % len(title_screen_frames)
        rocket_current_frame = (rocket_current_frame + 1) % len(rocket_frames)
        super_current_frame = (super_current_frame + 1) % len(super_frames)

    # Fill screen with white color before bliting
    screen.fill((255, 255, 255))

    # Blit image at (100, 150)
    screen.blit(title_screen_frames[title_screen_current_frame], (50, 100))
    screen.blit(rocket_frames[rocket_current_frame], (250, 100))
    screen.blit(super_frames[super_current_frame], (400, 100))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
