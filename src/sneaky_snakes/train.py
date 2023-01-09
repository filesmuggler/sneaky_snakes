import random
import pygame
from Agent import Agent
from GameAI import GameAI
from utilities import Direction

MAX_MEM = 100_000
BATCH_SIZE = 100
LR = 0.001
NUM_GAMES = 25

def run():
    g = GameAI()
    num_episodes = 10

    for no_ep in range(num_episodes):
        g.reset()
        episode_score = 0
        game_over = False
        # Run episode until it's over
        while not game_over:
            action = random.randrange(1,len(Direction)+1)
            reward, step_score, game_over = g.play_step(action)
            episode_score += step_score
        print("Final score after the ",no_ep+1," episode: ",episode_score)

def train():
    total_score = 0
    record_score = 0
    agent = Agent(batch=BATCH_SIZE,max_mem=MAX_MEM,lr=LR) # agent
    game = GameAI()
    for no_ep in range(NUM_GAMES):
        game.reset()
        game_over = False
        while not game_over:
            pass


if __name__ == '__main__':
   train()

