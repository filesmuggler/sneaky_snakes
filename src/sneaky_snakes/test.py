import random
import pygame
from Agent import Agent
from GameAI import GameAI
from utilities import Direction, Plotter

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001
NUM_GAMES = 10

def test():
    agent = Agent( batch=0,max_mem=0,lr=0,no_episodes=NUM_GAMES,path_to_model="./models/best_model_100g.pt",train=False) # agent
    game = GameAI()
    record_score = 0

    for no_ep in range(NUM_GAMES):
        game.reset()
        game_over = False
        print("Starting new episode no: ",no_ep+1)
        while not game_over:
            # get current state
            old_state = agent.get_state(environment=game)

            # get move
            final_move = agent.get_action(state=old_state)

            # perform move and get new state
            reward, score, done = game.play_step(action=final_move)
            new_state = agent.get_state(environment=game)

            game_over = done
            if done:
                # train over batch of memorized values
                agent.no_games += 1
                print('Game ',agent.no_games, ', score ',score,', record ',record_score)



if __name__ == '__main__':
   test()

