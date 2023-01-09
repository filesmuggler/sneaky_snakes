import torch
import random
import numpy as np
from collections import deque
from GameAI import GameAI
from utilities import Direction, Point

MAX_MEM = 100_000
BATCH_SIZE = 100
LR = 0.001

class Agent:
    def __init__(self, batch: int, max_mem: int, lr: float):
        '''
        Agent constructor
        Args:
            batch: number of samples to use in one batch training
            max_mem: maximal number of past states stored in the memory of the agent
            lr: learning rate
        '''
        self.batch_size = batch
        self.max_mem = max_mem
        self.lr = lr

        self.no_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=self.max_mem)
        #TODO: model and trainer

    def get_state(self, environment: GameAI) -> np.array:
        '''
        Returns the state of the environment - the obstacles in every direction,
        current direction of the agent and if food is nearby.
        State vector [0,1,0,1,0,0,0,0,0,0,0] -> snake going left with
        danger to the right from the head, no food to be seen nearby.
        Look for the ascii image below as a reference.
        _________________
        |     ########  |
        |               |
        | 🍎            |
        |_______________|
        Args:
            environment: game environment

        Returns:
            state vector with 11 int values
        '''
        head = environment.snake.get_head()

        #TODO: calculating state
        state = []
        return np.array(state,dtype=int)

    def save_to_memory(self, current_state: np.array, action, reward, next_state, done):
        '''
        Saves set of states, action, reward and status of the iteration to the memory
        Args:
            current_state: state the agent is coming from
            action: action he takes to go to the next state
            reward: reward to get in the next state
            next_state: the next state
            done: if the game is over or not

        Returns:
            void
        '''
        data_tuple = (current_state,action,reward,next_state,done)
        self.memory.append(data_tuple)

    def train_long_memory(self):
        # train the agent from batch of data saved in the memory
        if len(self.memory) > self.batch_size:
            batch_sample = random.sample(self.memory, self.batch_size)
        else:
            batch_sample = self.memory

        # TODO: train long memory

    def train_short_memory(self, current_state, action, reward, next_state, done):
        # TODO: train short memory
        pass

    def get_action(self, state):
        '''
        TODO: provide better epsilon estimation throughout the learning possibly rational function 1/(1+no_games)
        '''
        self.epsilon = 80 - self.no_games
        final_move = [0,0,0]
        #if random.randint(0, 200) < self.epsilon:
        #    move = random.randint(0, 2)
        #    final_move[move] = 1
        #else:
            #state0 = torch.tensor(state, dtype=torch.float)
            #prediction = self.model(state0)
            #move = torch.argmax(prediction).item()
            #final_move[move] = 1

        return final_move

