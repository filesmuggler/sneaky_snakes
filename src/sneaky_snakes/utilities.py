import pygame
import logging

class ColorPalette:
    def __init__(self):
        self.palette = {
            "black": pygame.Color(0,0,0),
            "white": pygame.Color(255,255,255),
            "red": pygame.Color(255,0,0),
            "green": pygame.Color(0,255,0),
            "blue": pygame.Color(0,0,255)
        }

    def get_palette(self) -> dict:
        return self.palette

    def get_color(self, color_key: str) -> pygame.Color:
        if color_key in self.palette:
            return self.palette[color_key]
        else:
            logging.warning(color_key + " not in the palette.\
                            Returning pygame.Color(255,0,0) instead")
            return self.palette['red']

    def add_color(self, color_key: str, red: int, green: int, blue: int) -> None:
        if color_key not in self.palette:
            self.palette[color_key] = pygame.Color(red,blue,green)
        else:
            logging.info(color_key + " already in the palette with value: ("+\
                str(self.palette[color_key].r) + ", "+\
                str(self.palette[color_key].g) + ", "+\
                str(self.palette[color_key].b) + ")")
        
    def update_color(self, color_key: str, red: int, green: int, blue: int) -> None:
        self.palette[color_key] = pygame.Color(red,blue,green)
        logging.info("color "+color_key+" updated with value: ("+\
                str(self.palette[color_key].r) + ", "+\
                str(self.palette[color_key].g) + ", "+\
                str(self.palette[color_key].b) + ")")

class Point:
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y

from enum import Enum
class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

