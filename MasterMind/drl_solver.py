# =============================================================================
# Generated with help from Microsoft AI Copilot (https://copilot.microsoft.com)
# =============================================================================
__author__ = "Kinas, Microsoft AI Copilot"
__copyright__ = "Copyright 2025, Vibe-Coding Project"
__credits__ = ["Kinas", "Microsoft AI Copilot"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kinas"
__email__ = "kinas.devops@gmail.com"
__status__ = "Production"
# =============================================================================

import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
from itertools import product

class QNet(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def forward(self, x):
        return self.fc(x)

def feedback(secret, guess):
    s, g = list(secret), list(guess)
    exact = sum(a == b for a, b in zip(s, g))
    s_used = [False]*len(s)
    g_used = [False]*len(s)
    for i in range(len(s)):
        if s[i] == g[i]:
            s_used[i] = g_used[i] = True
    partial = 0
    for i in range(len(s)):
        if not g_used[i]:
            for j in range(len(s)):
                if not s_used[j] and g[i] == s[j]:
                    s_used[j] = True
                    partial += 1
                    break
    return (exact, partial)

class DRLMastermindAgent:
    def __init__(self, colors="RGB", code_length=3, epsilon=0.2, lr=1e-3, gamma=0.95):
        self.colors = colors
        self.code_length = code_length
        self.actions = [''.join(p) for p in product(colors, repeat=code_length)]
        self.index = {code: i for i, code in enumerate(self.actions)}
        self.model = QNet(input_size=len(self.actions)*2, output_size=len(self.actions))
        self.target = QNet(input_size=len(self.actions)*2, output_size=len(self.actions))
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.memory = deque(maxlen=10000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = 64

    def state_vector(self, history):
        vec = np.zeros(len(self.actions)*2)
        for guess, (e, p) in history:
            gi = self.index[guess]
            vec[gi] = e
            vec[len(self.actions) + gi] = p
        return vec

    def choose(self, history, training=False):
        used = {g for g, _ in history}
        mask = [i for i, g in enumerate(self.actions) if g not in used]

        if training and random.random() < self.epsilon:
            return random.choice([self.actions[i] for i in mask]) if mask else random.choice(self.actions)

        state = torch.tensor([self.state_vector(history)], dtype=torch.float32)
        with torch.no_grad():
            qvals = self.model(state).squeeze()

        if not mask:
            return self.actions[qvals.argmax().item()]
        best_index = mask[qvals[mask].argmax().item()]
        return self.actions[best_index]

    def store(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        actions = torch.tensor([self.index[a] for a in actions])
        dones = torch.tensor(dones, dtype=torch.float32)

        q_vals = self.model(states)
        next_q_vals = self.target(next_states)

        q_action = q_vals[range(self.batch_size), actions]
        next_max = next_q_vals.max(1)[0]
        targets = rewards + self.gamma * next_max * (1 - dones)

        loss = nn.MSELoss()(q_action, targets.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target(self):
        self.target.load_state_dict(self.model.state_dict())