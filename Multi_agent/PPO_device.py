import numpy as np
import torch as T
import torch.nn as nn
import torch.optim as optim
import Multi_agent.settings as set
from torch.distributions.categorical import Categorical
import os

class PPOMemory:
    def __init__(self):
        self.episode, self.conflicts, self.crashs = 0, 0, 0
    
    @property
    def clear_memory(self):
        self.crashs, self.conflicts = 0, 0
        self.episode += 1

class PreProcessIntruders(nn.Module):
    def __init__(self):
        super(PreProcessIntruders, self).__init__()
        self.gru = nn.GRU(4, 4, batch_first=True)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, int_observ):
        int_observ = T.tensor(np.array(int_observ), dtype=T.float).to(self.device)
        out, hid = self.gru(int_observ.view(len(int_observ), 1, -1))
        return out[-1]

class ActorNetwork(nn.Module):
    def __init__(self):
        super(ActorNetwork, self).__init__()
        if not set.scenario==3:
            self.Fwd = nn.Sequential(
                nn.Linear(8, 256*4),
                nn.ReLU(),
                nn.Linear(256*4, 9),
                nn.Softmax(dim=-1))
        else:
            self.Fwd = nn.Sequential(
                nn.Linear(7, 256*4),
                nn.ReLU(),
                nn.Linear(256*4, 9),
                nn.Softmax(dim=-1))
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        dist = self.Fwd(T.tensor(state, dtype=T.float).to(self.device))
        return Categorical(dist)

class SuperAgent:
    def __init__(self):
        super(SuperAgent, self).__init__()
        self.Policy, self.gru, self.memory   = ActorNetwork(), PreProcessIntruders(), PPOMemory()
        print(f'\n\n--LOADING MODELS--\n')
        if set.os == 'L':
            self.Policy.load_state_dict(T.load(os.getcwd()+'/Multi_agent/Models/Actor_'+str(set.scenario)))
            self.gru.load_state_dict(T.load(os.getcwd()+'/Multi_agent/Models/Gru_'+str(set.scenario)), strict=False)
        else:
            self.Policy.load_state_dict(T.load(os.getcwd()+'\\Multi_agent\\Models\\Actor_'+str(set.scenario)))
            self.gru.load_state_dict(T.load(os.getcwd()+'\\Multi_agent\\Models\\Gru_'+str(set.scenario)), strict=False)
        self.Policy.eval()
        self.gru.eval()

    def remember(self, agent):
        self.memory.conflicts += agent.conflicts
        self.memory.crashs += agent.crashs

    def choose_action(self, agent):
        with T.no_grad():
            own_state = T.tensor(agent.state[0], dtype=T.float).to(self.Policy.device)
            processed_state = T.cat(tuple([own_state, T.squeeze(self.gru(agent.state[1:]))]))
            dist   = self.Policy(processed_state)
            action = dist.sample()
            agent.action_idx = T.squeeze(action).item()
