import torch
import random
import numpy as np
from collections import deque
from GameAI import GameAI
from utilities import Direction, Point
from models import Linear_Net, DQN_Trainer

#TODO: remove constants from files other than train.py
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
        self.model = Linear_Net(11, 256, 3)
        self.trainer = DQN_Trainer(self.model,lr=LR,gamma=self.gamma)

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

        # Get current direction
        dir_left, dir_up, dir_right, dir_down = self.get_current_direction(environment=environment)
        # Get surround information
        pt_left, pt_up, pt_right, pt_down = self.get_surround(environment)
        # Check if food nearby
        food_left, food_up, food_right, food_down = self.get_food_nearby(environment)

        danger_left = (dir_down and environment.is_collision(pt_right)) or (
                    dir_up and environment.is_collision(pt_left)) or \
                      (dir_right and environment.is_collision(pt_up)) or (
                                  dir_left and environment.is_collision(pt_down))

        danger_straight = (dir_down and environment.is_collision(pt_down)) or (
                    dir_up and environment.is_collision(pt_up)) or \
                      (dir_right and environment.is_collision(pt_right)) or (
                                  dir_left and environment.is_collision(pt_left))

        danger_right = (dir_down and environment.is_collision(pt_left)) or (
                    dir_up and environment.is_collision(pt_right)) or \
                      (dir_right and environment.is_collision(pt_down)) or (
                                  dir_left and environment.is_collision(pt_up))

        state = [danger_left,danger_straight,danger_right,
                 dir_left,dir_up,dir_right,dir_down,
                 food_left,food_up,food_right,food_down]
        return np.array(state,dtype=int)

    def get_current_direction(self,environment: GameAI) -> list[bool]:
        dir_left = environment.direction == Direction.LEFT
        dir_up = environment.direction == Direction.UP
        dir_right = environment.direction == Direction.RIGHT
        dir_down = environment.direction == Direction.DOWN
        return [dir_left,dir_up,dir_right,dir_down]

    def get_food_nearby(self,environment: GameAI) -> list[bool]:
        '''
            Checks food proximity in clockwise direction starting from LEFT
        Args:
            environment:

        Returns:
            Boolean list of food position wrt to the snake head
        '''

        pt = environment.snake.get_head()

        # Check if food nearby
        # TODO: quite limited perception -> widen the perception field

        fruit_pos = environment.fruit.get_position()
        food_left = (fruit_pos.x < pt.x)
        food_up = (fruit_pos.y < pt.y)
        food_right = (fruit_pos.x > pt.x)
        food_down = (fruit_pos.y > fruit_pos.y)

        return [food_left,food_up,food_right,food_down]

    def get_surround(self, environment: GameAI) -> list[Point]:
        '''
            Calculates points in the clockwise direction starting from LEFT
        Args:
            environment:

        Returns:

        '''
        scale = environment.scale
        pt = environment.snake.get_head()

        # Get coordinates of the points around head
        pt_left, pt_up, pt_right, pt_down = Point(pt.x - scale,pt.y), Point(pt.x,pt.y-scale), \
                                                    Point(pt.x+scale,pt.y), Point(pt.x,pt.y+scale)

        return [pt_left, pt_up, pt_right, pt_down]

    def get_action(self, state) -> list[int]:
        '''

        Args:
            state: agent state

        Returns:
            final_move: [straight,right,left] array of 1s and 0s
        '''
        '''
        TODO: provide better epsilon estimation throughout the learning possibly rational function 1/(1+no_games)
        '''
        self.epsilon = 80 - self.no_games
        final_move = [0,0,0] #[straight,right,left]
        if random.randint(0, 200) < self.epsilon:
           move = random.randint(0, 2)
           final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


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
        # trained over larger number of samples at the same time
        if len(self.memory) > self.batch_size:
            batch_sample = random.sample(self.memory, self.batch_size)
        else:
            batch_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*batch_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self, current_state, action, reward, next_state, done):
        # train agent for the batch of data equal to 1
        self.trainer.train_step(current_state,action,reward,next_state,done)


