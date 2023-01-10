import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_Net(nn.Module):
    '''
    Linear model implementation
    '''
    def __init__(self,input_size: int, hidden_size: int,output_size: int):
        super().__init__()
        self.linear_layer_1 = nn.Linear(input_size,hidden_size)
        self.linear_layer_2 = nn.Linear(hidden_size,output_size)

    def forward(self,x):
        x = F.relu(self.linear_layer_1(x))
        x = self.linear_layer_2(x)
        return x

    def save(self,file_name):
        model_folder_path = './models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path,file_name)
        torch.save(self.state_dict(),file_name)

class DQN_Trainer:
    def __init__(self, model: Linear_Net, lr: float, gamma: float):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done: bool):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action,dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n,x) == (n batches, values)

        if len(state.shape) == 1:
            # (1,x) == (number of batches,values)
            state = torch.unsqueeze(state,0)
            next_state = torch.unsqueeze(next_state,0)
            action = torch.unsqueeze(action,0)
            reward = torch.unsqueeze(reward,0)
            done = (done,)

        # predicted Q values with current state
        # returns 3 values
        pred = self.model(state)

        target = pred.clone()
        # everything should be the same size
        # idx is just used for iterating over the batch inputs
        for idx in range(len(done)):
            # for every set of values in the batch calculate the following
            # initially Q_new equals respective reward but if not done at give batch input
            # then calculate Q_new with bellman equation
            Q_new = reward[idx]
            if not done[idx]:
                # Q_new = reward at given state + discounted value of next predicted state
                #
                # torch.max() produces the maximum VALUE of all elements in the tensor
                # the model returns 3 values -> action tensor; should the agent continue forward
                # or go either left or right in the next step
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # torch.argmax() returns the INDEX of the maximum value of all elements in the tensor
            # torch.argmax(action[idx]).item() -> the value of the index of maximum value of action[idx] tensor
            # target[idx][torch.argmax(action[idx]).item()] = Q_new -> setting the idx-th target value of action to
            # the new Q_new ?
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Q_new = reward + gamma*max(Q_value_at_next_state)
        self.optimizer.zero_grad()
        loss = self.criterion(target,pred)
        loss.backward()

        self.optimizer.step()


