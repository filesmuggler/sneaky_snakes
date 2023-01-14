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

    def set_direction(self, direction: Direction):
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
    def move(self, action: list[int]):
        '''
        Moves snake's body forward in the given direction
        Args:
            action: int list [straight, right, left]

        Returns:
            void
        '''

        clock_wise = [Direction.LEFT,Direction.UP,Direction.RIGHT,Direction.DOWN]
        idx = clock_wise.index(self.direction)

        # [1,0,0] -> if right, continue right
        # [0,1,0] > if right, go down
        # [0,0,1] -> if right, go up

        # calculate ne direction
        if np.array_equal(action,[1,0,0]):
            # continue the direction you were going
            new_direction = self.direction
        elif np.array_equal(action,[0,1,0]):
            # go right wrt the direction you were b4
            cycle_idx = (idx+1)%4
            new_direction = clock_wise[cycle_idx]
        elif np.array_equal(action,[0,0,1]):
            # go left wrt the direction you were b4
            cycle_idx = (idx - 1) % 4
            new_direction = clock_wise[cycle_idx]
        else:
            print("invalid action. terminating game. action: ",action)

        # SET new direction
        self.set_direction(direction=new_direction)

        # moving snake
        if self.direction == Direction.UP:
            self.head[1] -= self.scale
        if self.direction == Direction.DOWN:
            self.head[1] += self.scale
        if self.direction == Direction.LEFT:
            self.head[0] -= self.scale
        if self.direction == Direction.RIGHT:
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



