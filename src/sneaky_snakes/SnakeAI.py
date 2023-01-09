import pygame
import random
from utilities import Direction, Point
import numpy as np

class SnakeAI:
    def __init__(self, color: pygame.Color, tick: int, direction:Direction, scale=10, x=100, y=50):
        '''
        Snake constructor
        Args:
            color: snake color
            tick: snake speed
            direction: snake initial direction
            scale: how thick the snake should be
            x: starting position X
            y: starting position Y
        '''
        # System wide settings
        self.scale = scale
        self.color = color
        self.speed = tick
        self.direction = direction
        #
        self.reset(x=x,y=y,dir=direction)

    def get_head(self) -> Point:
        '''
        Returns head position of the snake
        Returns:
            Returns tuple of (x,y) coordinates
        '''
        return Point(self.body[0][0],self.body[0][1])

    def set_direction(self,direction: Direction):
        '''
        Sets direction of the snake
        Args:
            direction:

        Returns:
            void
        '''
        self.direction = direction

    def get_direction(self):
        '''
        Returns direction the snake is headed to
        Returns:
            Direction enum type
        '''
        return self.direction
    def move(self, direction: Direction):
        '''
        Moves snake's body forward in the given direction
        Args:
            direction: enum type Direction

        Returns:
            void
        '''

        self.set_direction(direction)

        #moving snake
        if direction == Direction.UP:
            self.head[1] -= self.scale
        if direction == Direction.DOWN:
            self.head[1] += self.scale
        if direction == Direction.LEFT:
            self.head[0] -= self.scale
        if direction == Direction.RIGHT:
            self.head[0] += self.scale


    def cut_tail(self):
        '''
        Keeps the size of the snake the same as iteration before
        Returns:
            void
        '''
        self.body.pop()

    def grow_body(self):
        '''
        Adds a component to the snake body
        Returns:
            void
        '''
        self.body.insert(0, list(self.head))

    def reset(self, x:int, y:int, dir: Direction):
        '''
        Resets the snake state for the new game
        Args:
            x: starting position X
            y: starting position Y
            dir: starting direction of eunm type Direction

        Returns:
            void
        '''
        self.head = [x,y]
        self.body = [[x,y],
                    [x-1*self.scale,y],
                    [x-2*self.scale,y],
                    [x-3*self.scale,y]]
        self.direction = dir



