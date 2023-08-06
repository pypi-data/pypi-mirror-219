import pygame


class Image:
    def __init__(self, image, size):
        self.image = pygame.image.load(image)
        self.size = size


class Color:
    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
