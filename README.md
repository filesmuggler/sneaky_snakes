# Reinforcement learning with snake in pygame
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![pytorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

![snake1](./src/docs/snake1_small.gif)
![snake1](./src/docs/snake2_small.gif)
![snake1](./src/docs/snake3_small.gif)
![snake1](./src/docs/snake4_small.gif)

## Background
### Reinforcement learning basics

![diagram](./src/docs/reinforcement.jpg)

#### _Agent_
The agent is an entity that can enforce actions on the environment 
and observe changes in it. According to the actions it takes, it is 
rewarded or punished in the process of learning. In our case the agent is 
replacing the human player in the process of controlling the snake.
#### _Environment_
The environment consists the table, the apple and the snake. 
They provide the information about current state and rewards for the actions
taken by the agent

![table](./src/docs/snake_diagram.jpg)

#### _Action_
The action is taken by the agent and is affecting the environment. 
#### _Reward_
The reward is assigned based on the performance of the agent in the environment. 
The agent gets positive reward for getting the apple and negative for hitting walls/himself
or exceeding the time intended for exploration.

## Perception

The agent is able to _sniff_ food in 4 main directions - left,up,right,down.
Sniffing is based on position of the fruit obtained from the game environment and
projected as boolean list of directions.

![perception](./src/docs/perception.png)



## The Agent

## Training

### Neural net model

Used model is fully connected network built of two linear layers.<br>
<img src="./src/docs/LinearNet.png" height="200">

### Deep Q-Learning (DQN)


## Testing



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