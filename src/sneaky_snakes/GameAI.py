import pygame
import random

from SnakeAI import SnakeAI
from Fruit import Fruit
from Table import Table
from utilities import Direction, ColorPalette

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TICK = 15
SCALE = 10

class GameAI:
    def __init__(self):
        self.cp_object = ColorPalette()
        self.cpalette = self.cp_object.get_palette()
        self.reset()

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

        # 1. setup
        self.iterations += 1
        reward = 0
        game_over = False

        # 2. move snake
        self.snake.move(direction=action)

        # 3. check if got fruit
        if self.check_fruit():
            reward = 10
            self.score += 10
            self.snake.grow_body()
            self.spawn_fruit()
        else:
            self.snake.grow_body()
            self.snake.cut_tail()

        # 4. check if collision or too long searching for food
        if self.is_collision() or self.iterations > 100*len(self.snake.body):
            reward = -10
            game_over = True
            # break the function and return immediately to the main loop
            return reward, self.score, game_over

        # 5. draw everything
        self.game_window.fill(self.cpalette["black"])
        for pos in self.snake.body:
            pygame.draw.rect(self.game_window, self.snake.color,
                             pygame.Rect(pos[0], pos[1], self.scale, self.scale))
        pygame.draw.rect(self.game_window, self.fruit.color,
                         pygame.Rect(self.fruit.position[0], self.fruit.position[1],
                                     self.scale, self.scale))

        # 6. show score
        self.show_score(self.cpalette['green'], 'consolas', 37)

        # 7. update pygame window
        pygame.display.update()
        self.fps.tick(TICK)

        # 8. return
        return reward, self.score, game_over

    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        
        score_rect = score_surface.get_rect()
        
        self.game_window.blit(score_surface, score_rect)

    def spawn_fruit(self):
        new_position = self.random_position()
        self.fruit.set_position(new_position)

    def is_collision(self):
        if self.snake.head[0] < 0 or self.snake.head[0] > self.game_window.get_size()[0]:
            return True
        elif self.snake.head[1] < 0 or self.snake.head[1] > self.game_window.get_size()[1]:
            return True
        else:
            return False

    def check_fruit(self) -> bool:
        if self.snake.head[0] == self.fruit.position[0] and \
        self.snake.head[1] == self.fruit.position[1]:
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

