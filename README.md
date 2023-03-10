# Reinforcement learning with snake in pygame
[![license](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![pygame](https://img.shields.io/badge/PyGame-00FF00?style=for-the-badge)](https://www.pygame.org/news)
[![pytorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![numpy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![matplotlib](https://img.shields.io/badge/Matplotlib-%23b0b0b0.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)](https://matplotlib.org/)

![snake1](docs/images/snake1_small.gif)
![snake1](docs/images/snake2_small.gif)
![snake1](docs/images/snake3_small.gif)
![snake1](docs/images/snake4_small.gif)

## RL building blocks

![diagram](docs/images/reinforcement.jpg)

### Agent
The agent is an entity that can enforce actions on the environment 
and observe changes in it. According to the actions it takes, it is 
rewarded or punished in the process of training. It's learning itself
through trial and error and receives rewards as unique feedback. 
In our case the agent is replacing the human player in the process 
of controlling the snake.

Configurable parameters:
- _MAX_MEM_ - maximal number of sets of states stored for the training
- _BATCH_SIZE_ - size of single batch to train on
- _LR_ - learning rate

#### _Perception_

The agent is able to _sniff_ food in 4 main directions - left,up,right,down.
Sniffing is based on position of the fruit obtained from the game environment and
projected as boolean list of directions.

![perception](docs/images/perception.png)

### Environment
The environment consists the table, the apple and the snake. 
They provide the information about current state and rewards for the actions
taken by the agent. In our case the environment is represented by following classes: 
`GameAI`, `SnakeAI`, `Fruit` and `Table`. The input for environment is agent's action 
and the outputs are observation and reward for the step or set of steps.

Configurable parameters:
- _SCREEN_WIDTH_ - table width
- _SCREEN_HEIGHT_ - table height
- _TICK_ - how fast should the snake move
- _SCALE_ - how wide the snake should be

![table](docs/images/snake_diagram.jpg)

### Action
The action is taken by the agent and is affecting the environment, 
more specifically the snake's next move. In our case action is represented as 
a list of 0's and 1's according to the following schema: `[straight, right, left]`.

![direction](docs/images/direction.jpg)

Example:
- `[1,0,0]` means go straight wrt to the snake's head direction (choosing <span style="color:purple">purple</span> arrow)
- `[0,1,0]` means go straight wrt to the snake's head direction (choosing <span style="color:orange">orange</span> arrow)
- `[0,0,1]` means go straight wrt to the snake's head direction (choosing <span style="color:cyan">cyan</span> arrow)

### Reward
The reward is assigned based on the performance of the agent in the environment. 
The agent gets positive reward for getting the apple and negative for hitting walls/himself
or exceeding the time intended for exploration.

## Neural net model

Used model is fully connected network built of two linear layers.<br>
![net](docs/images/LinearNet.png)

## Deep Q-Learning (DQN)

The Deep Q-Learning is using a neural network, in our case a fully connected one, 
to approximate, given a state, the different Q-values for each possible action at that state. 
We use `DQN_Trainer` to train the agent with Q-value estimation. We create a loss function 
that compares our Q-value prediction for given state and the Q-target, which is the output of
the model in this case.

_See more at [HuggingFace tutorial](https://huggingface.co/deep-rl-course/unit3/deep-q-network?fw=pt)_

## Play around

### Prepare python environment
Clone repository: 
```shell
cd ~/
git clone https://github.com/filesmuggler/sneaky_snakes.git
```
Create and activate virtual environment in Python
```shell
cd sneaky_snakes
python3 -m venv ./snake_env
source ./snake_env/bin/activate
```
Install packages from requirements into the virtual environment
```shell
python3 -m pip install -r requirements.txt
```

## Training

Run command:
```shell
python train.py --learning_rate 0.001 --max_mem 100000 --num_games 1000 --batch_size 1000 --width 400 --height 300 --tick 250 --scale 10
```

The model will be saved at the end of the session into the `models` directory.

## Testing

Run command:
```shell
python test.py --model_path "./models/best_model_so_far.pt" --num_games 10 --width 400 --height 300 --tick 10 --scale 10
```


## Bibliography

_Coding_
- [GeeksForGeeks](https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/) tutorial on creating snake game in Pygame from scratch
- [FreeCodeCamp.org](https://www.youtube.com/watch?v=L8ypSXwyBds) tutorial on turning snake into AI project

_Theory_
- [HuggingFace](https://huggingface.co/deep-rl-course/unit3/deep-q-network?fw=pt) guide on deep Q-Learning

## Further reading
- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [Artificial Intelligence: Foundations of Computational Agents](http://www.cambridge.org/9781107195394)
- [Pytorch documentation](https://pytorch.org/docs/stable/index.html)
- [Pygame documentation](https://www.pygame.org/docs/)