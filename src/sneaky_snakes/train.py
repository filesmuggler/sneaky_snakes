import argparse

from Agent import Agent
from GameAI import GameAI
from utilities import Plotter

def train(**args):
    plot_scores = []
    plot_mean_scores = []

    args = args['args']
    LR = float(args.learning_rate)
    MAX_MEM = int(args.max_mem)
    NUM_GAMES = int(args.num_games)
    BATCH_SIZE = int(args.batch_size)
    SCREEN_WIDTH = int(args.width)
    SCREEN_HEIGHT = int(args.height)
    TICK = int(args.tick)
    SCALE = int(args.scale)

    total_score = 0
    record_score = 0
    agent = Agent(batch=BATCH_SIZE,max_mem=MAX_MEM,lr=LR, no_episodes=NUM_GAMES, train=True, path_to_model="") # agent
    game = GameAI(screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT, tick=TICK, scale=SCALE) # game

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-vv", "--version", help="show program version", action="store_true")
    parser.add_argument("-mm", "--max_mem", help="maximal number of sets of states stored for the training")
    parser.add_argument("-bs", "--batch_size", help="size of single batch to train on")
    parser.add_argument("-lr", "--learning_rate", help="learning rate")
    parser.add_argument("-ng", "--num_games", help="number of games")
    parser.add_argument("-tw", "--width", help="table width", )
    parser.add_argument("-th", "--height", help="table height")
    parser.add_argument("-tk", "--tick", help="how fast should the snake move")
    parser.add_argument("-sc", "--scale", help="how wide the snake should be")

    args = parser.parse_args()

    train(args=args)

