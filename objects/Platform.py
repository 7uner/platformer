import pygame


class Platform:
    def __init__(self, x, y, width, height):
        self.platform = pygame.Rect(x, y, width, height)


class Coin:
    def __init__(self, x, y):
        self.coin = pygame.Rect(x, y, 50, 50)