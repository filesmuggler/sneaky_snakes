import pygame

class Table:
    def __init__(self, window_width: int, window_height: int, color: pygame.Color):
        self.width = window_width
        self.height = window_height
        self.color = color