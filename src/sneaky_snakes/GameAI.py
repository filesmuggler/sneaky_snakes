import pygame
import time
import random

from utilities import ColorPalette
from SnakeAI import SnakeAI
from Fruit import Fruit
from Table import Table
from Direction import Direction

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TICK = 15
SCALE = 10

class GameAI:
    def __init__(self):
        self.cp_object = ColorPalette()
        self.cpalette = self.cp_object.get_palette()
        self.reset()

    # reset
    # reward
    # play(action) -> direction
    # game_iteration
    # is_collision

    def reset(self):
        self.snake = SnakeAI(color=self.cpalette["white"], tick=TICK)
        self.fruit = Fruit(color=self.cpalette["red"], window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT)
        self.table = Table(color=self.cpalette["black"], window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT)
        self.scale = SCALE

        pygame.init()
        # Initialise game window
        pygame.display.set_caption('Sneaky Snakes')
        self.game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.score = 0
        self.is_game_over = False
        self.iterations = 0


    def user_input(self):
        change_to = ''

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = Direction.UP
                if event.key == pygame.K_DOWN:
                    change_to = Direction.DOWN
                if event.key == pygame.K_LEFT:
                    change_to = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    change_to = Direction.RIGHT

        #prevent simulataneous movement in two directions
        if change_to == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if change_to == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        if change_to == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        if change_to == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

        return self.direction

    def play_step(self, action: int):

        self.iterations += 1

        self.snake.move(direction=action)
        got_fruit = self.check_fruit()
        self.snake.update(got_fruit=got_fruit)
        game_over = self.check_collision()

        # draw everything
        self.game_window.fill(self.cpalette["black"])
        for pos in self.snake.body:
            pygame.draw.rect(self.game_window, self.snake.color,
                             pygame.Rect(pos[0], pos[1], self.scale, self.scale))
        pygame.draw.rect(self.game_window, self.fruit.color,
                         pygame.Rect(self.fruit.position[0], self.fruit.position[1],
                                     self.scale, self.scale))

        self.show_score(self.cpalette['green'], 'consolas', 37)

        pygame.display.update()
        self.fps.tick(TICK)

        return self.score, game_over



    def run(self):
        while not self.is_game_over:
            direction = self.user_input()
            self.snake.move(direction=direction)
            
            got_fruit = self.check_fruit()
            self.snake.update(got_fruit=got_fruit)
            self.check_collision()

            # draw everything
            self.game_window.fill(self.cpalette["black"])
            for pos in self.snake.body:
                pygame.draw.rect(self.game_window, self.snake.color, 
                                 pygame.Rect(pos[0],pos[1],self.scale,self.scale))
            pygame.draw.rect(self.game_window, self.fruit.color,
                             pygame.Rect(self.fruit.position[0],self.fruit.position[1],
                                         self.scale, self.scale))

            self.show_score(self.cpalette['green'], 'consolas', 37)

            pygame.display.update()
            self.fps.tick(TICK)

    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        
        score_rect = score_surface.get_rect()
        
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):

        score_font = pygame.font.SysFont("consolas", 21)
        
        game_over_surface = score_font.render('Press any key to play again or Q to quit', True, self.cpalette["green"])
        
        game_over_rect = game_over_surface.get_rect(midtop=(SCREEN_WIDTH/2,300))
        
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()
            else:
                self.spawn_fruit()
                self.direction = self.random_direction()
                self.snake.reset(x=100,y=50, dir=self.direction)
                self.score = 0

    def spawn_fruit(self):
        new_position = self.fruit.random_position()
        self.fruit.set_position(new_position)

    def check_collision(self):
        if self.snake.head[0] < 0 or self.snake.head[0] > self.game_window.get_size()[0]:
            return True
        elif self.snake.head[1] < 0 or self.snake.head[1] > self.game_window.get_size()[1]:
            return True
        else:
            return False

    def check_fruit(self) -> bool:
        if self.snake.head[0] == self.fruit.position[0] and \
        self.snake.head[1] == self.fruit.position[1]:
            self.score += 10
            self.spawn_fruit()
            return True
        else:
            return False

    def random_position(self) -> list[int]:
        position = [random.randrange(1, (self.window_width // self.scale)) * self.scale,
                    random.randrange(1, (self.window_height // self.scale)) * self.scale]
        return position

    def random_direction(self) -> int:
        direction = random.randrange(1,len(Direction)+1)
        return direction



if __name__ == "__main__":

    g = GameAI()

    game_over = False
    score = 0

    while not game_over:
        # get action
        action = random.randrange(1, len(Direction) + 1)
        score, game_over = g.play_step(action)
    print("Final score ",score, " after ",g.iterations," steps.")

