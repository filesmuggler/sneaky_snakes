import pygame
from utilities import ColorPalette
from Snake import Snake
from Fruit import Fruit
from Table import Table

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TICK = 15
SCALE = 10

class Game:
    '''
    Main game class
    '''
    def __init__(self, snake: Snake, fruit: Fruit, table: Table, palette: ColorPalette, scale: int):
        '''
        Constructor method
        Args:
            snake: user controlled game agent
            fruit: goal
            table: settings for the background
            palette: set of colors
            scale: how thick the table grid should be
        '''
        self.snake = snake
        self.fruit = fruit
        self.table = table
        self.palette = palette
        self.scale = scale

        pygame.init()
        # Initialise game window
        pygame.display.set_caption('Sneaky Snakes')
        self.game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()   

        # Game parameters
        self.score = 0
        self.is_game_over = False

    def run(self) -> None:
        '''
        Main game loop
        Returns:
        None
        '''
        while not self.is_game_over:
            # get user input
            # TODO: move user input to the game itself; add move() method for snake
            self.snake.user_input()

            # check if fruit got picked during movement
            got_fruit = self.check_fruit()

            # update snake state
            self.snake.update(got_fruit=got_fruit)
            # check if snake did not hit the wall
            self.check_collision()

            # draw background
            self.game_window.fill(self.palette.get_palette()["black"])
            # draw snake
            for pos in self.snake.body:
                pygame.draw.rect(self.game_window, self.snake.color, 
                                 pygame.Rect(pos[0],pos[1],self.scale,self.scale))
            # draw fruit
            pygame.draw.rect(self.game_window, self.fruit.color,
                             pygame.Rect(self.fruit.position[0],self.fruit.position[1],
                                         self.scale, self.scale))

            # draw text with score
            self.show_score(self.palette.get_palette()['green'], 'consolas', 37)

            # update pygame mechanism
            pygame.display.update()
            self.fps.tick(TICK)

        return None


    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        
        score_rect = score_surface.get_rect()
        
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):

        score_font = pygame.font.SysFont("consolas", 21)
        
        game_over_surface = score_font.render('Press any key to play again or Q to quit', True, self.palette.get_palette()["green"])
        
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
                self.snake.respawn(x=100,y=50)
                self.score = 0


    def spawn_fruit(self):
        new_position = self.fruit.random_position()
        self.fruit.set_position(new_position)

    def check_collision(self):
        if self.snake.position[0] < 0 or self.snake.position[0] > self.game_window.get_size()[0]:
            self.game_over()
        if self.snake.position[1] < 0 or self.snake.position[1] > self.game_window.get_size()[1]:
            self.game_over()
        

    def check_fruit(self) -> bool:
        if self.snake.position[0] == self.fruit.position[0] and \
        self.snake.position[1] == self.fruit.position[1]:
            self.score += 10
            self.spawn_fruit()
            return True
        else:
            return False



if __name__ == "__main__":

    cp = ColorPalette()
    p = cp.get_palette()

    f = Fruit(color=p["red"], window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT)
    s = Snake(color=p["white"], tick=TICK)
    t = Table(color=p["black"], window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT)

    g = Game(fruit=f,snake=s,table=t, palette=cp, scale=SCALE)
    g.run()