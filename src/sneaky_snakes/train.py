import random

import pygame
from GameAI import GameAI
from Direction import Direction

def train():
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

if __name__ == '__main__':
   train()