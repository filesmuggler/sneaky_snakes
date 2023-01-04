import pygame

class Snake:
    def __init__(self, color: pygame.Color, tick: int, scale=10, x=100, y=50):
        self.scale = scale
        self.color = color
        self.speed = tick
        self.position = [x, y] # in pixels
        self.body = [[x,y],
                    [x-1*scale,y],
                    [x-2*scale,y],
                    [x-3*scale,y]]
        self.direction = 'R' # RIGHT
        self.change_to = self.direction


    def user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'U'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'D'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'L'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'R'

        #prevent simulataneous movement in two directions
        if self.change_to == 'U' and self.direction != 'D':
            self.direction = 'U'
        if self.change_to == 'D' and self.direction != 'U':
            self.direction = 'D'
        if self.change_to == 'L' and self.direction != 'R':
            self.direction = 'L'
        if self.change_to == 'R' and self.direction != 'L':
            self.direction = 'R'

        #moving snake
        if self.direction == 'U':
            self.position[1] -= self.scale
        if self.direction == 'D':
            self.position[1] += self.scale
        if self.direction == 'L':
            self.position[0] -= self.scale
        if self.direction == 'R':
            self.position[0] += self.scale

    def update(self, got_fruit=False):
        self.body.insert(0, list(self.position))
        if not got_fruit:
            self.body.pop()

    def respawn(self, x:int, y:int):
        #TODO: better implementation - randomized values
        self.position = [x, y] # in pixels
        self.body = [[x,y],
                    [x-1*self.scale,y],
                    [x-2*self.scale,y],
                    [x-3*self.scale,y]]
        self.direction = 'R' # RIGHT
        self.change_to = self.direction



