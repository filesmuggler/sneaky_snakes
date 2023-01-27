import random
import pygame
from Agent import Agent
from GameAI import GameAI
from utilities import Direction, Plotter

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001
NUM_GAMES = 1000

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent(batch=BATCH_SIZE,max_mem=MAX_MEM,lr=LR, no_episodes=NUM_GAMES, train=True, path_to_model="") # agent
    game = GameAI()

    for no_ep in range(NUM_GAMES):
        game.reset()
        game_over = False
        print("Starting new episode no: ",no_ep+1)
        while not game_over:
            # get current state
            old_state = agent.get_state(environment=game)

            # get move
            final_move = agent.get_action(state=old_state, train=True)

            # perform move and get new state
            reward, score, done = game.play_step(action=final_move)
            new_state = agent.get_state(environment=game)

            # train short memory
            agent.train_short_memory(current_state=old_state,action=final_move,
                                     reward=reward,next_state=new_state,done=done)
            # remember
            agent.save_to_memory(current_state=old_state,action=final_move,
                                 reward=reward,next_state=new_state,done=done)

            game_over = done    # check if game is over
            if done:
                # train over batch of memorized values
                agent.no_games += 1
                agent.train_long_memory()

                if score > record_score:
                    record_score = score
                    agent.model.save('best_model.pt')

                print('Game ',agent.no_games, ', score ',score,', record ',record_score)

                # accumulate metrics
                plot_scores.append(score)
                total_score += score
                mean_score = total_score/agent.no_games
                plot_mean_scores.append(mean_score)
    # plot scores
    plotter = Plotter()
    plotter.plot(plot_scores,plot_mean_scores)


if __name__ == '__main__':
   train()

