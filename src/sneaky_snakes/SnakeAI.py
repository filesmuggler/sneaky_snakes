import pygame
import random
from Direction import Direction

class SnakeAI:
    def __init__(self, color: pygame.Color, tick: int, scale=10, x=100, y=50):
        # System wide settings
        self.scale = scale
        self.color = color
        self.speed = tick
        #
        self.reset(x=x,y=y,dir='R')

    def set_direction(self,direction: int):
        self.direction = direction

    def get_direction(self):
        return self.direction
    def move(self, direction: int):

        self.set_direction(direction)

        dir_temp = Direction(self.direction)

        #moving snake
        if dir_temp == Direction.UP:
            self.head[1] -= self.scale
        if dir_temp == Direction.DOWN:
            self.head[1] += self.scale
        if dir_temp == Direction.LEFT:
            self.head[0] -= self.scale
        if dir_temp == Direction.RIGHT:
            self.head[0] += self.scale

    def cut_tail(self):
        self.body.pop()

    def grow_body(self):
        self.body.insert(0, list(self.head))

    def reset(self, x:int, y:int, dir: int):
        self.head = [x,y]
        self.body = [[x,y],
                    [x-1*self.scale,y],
                    [x-2*self.scale,y],
                    [x-3*self.scale,y]]
        self.direction = dir # RIGHT



