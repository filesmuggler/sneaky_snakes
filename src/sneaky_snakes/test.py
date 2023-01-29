import argparse
from Agent import Agent
from GameAI import GameAI

def test(**args):
    args = args['args']
    NUM_GAMES = int(args.num_games)
    PATH_MODEL = args.model_path
    SCREEN_WIDTH = int(args.width)
    SCREEN_HEIGHT = int(args.height)
    TICK = int(args.tick)
    SCALE = int(args.scale)

    agent = Agent(batch=0,max_mem=0,lr=0,no_episodes=NUM_GAMES,path_to_model=PATH_MODEL,train=False) # agent
    game = GameAI(screen_width=SCREEN_WIDTH,screen_height=SCREEN_HEIGHT, tick=TICK, scale=SCALE) # game
    record_score = 0

    for no_ep in range(NUM_GAMES):
        game.reset()
        game_over = False
        print("Starting new episode no: ",no_ep+1)
        while not game_over:
            # get current state
            old_state = agent.get_state(environment=game)

            # get move
            final_move = agent.get_action(state=old_state, train=False)

            # perform move and get new state
            reward, score, done = game.play_step(action=final_move)
            new_state = agent.get_state(environment=game)

            game_over = done
            if done:
                if score > record_score:
                    record_score = score

                agent.no_games += 1
                print('Game ',agent.no_games, ', score ',score,', record ',record_score)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-vv", "--version", help="show program version", action="store_true")
    parser.add_argument("-mp", "--model_path", help="path to model")
    parser.add_argument("-ng", "--num_games", help="number of games")
    parser.add_argument("-tw", "--width", help="table width", )
    parser.add_argument("-th", "--height", help="table height")
    parser.add_argument("-tk", "--tick", help="how fast should the snake move")
    parser.add_argument("-sc", "--scale", help="how wide the snake should be")

    args = parser.parse_args()
    test(args=args)

