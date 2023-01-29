import pygame
import random

from utilities import Point

class Fruit:
    def __init__(self, color: pygame.Color, 
                 window_width: int, window_height: int,
                 scale=10):
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.position = self.random_position()
        self.color = color

    def random_position(self) -> list[int]:
        position = [random.randrange(1, (self.window_width//10)) * self.scale,
				        random.randrange(1, (self.window_height//10)) * self.scale]
        return position

    def set_position(self,position: list) -> None:
        self.position = position
        return None

    def get_position(self):
        return Point(self.position[0],self.position[1])