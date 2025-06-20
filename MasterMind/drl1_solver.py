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

COLORS = "RGB"
CODE_LENGTH = 3
ALL_CODES = [''.join(p) for p in product(COLORS, repeat=CODE_LENGTH)]
CODE_INDEX = {code: i for i, code in enumerate(ALL_CODES)}

def feedback(secret, guess):
    s, g = list(secret), list(guess)
    exact = sum([a == b for a, b in zip(s, g)])
    s_used = [False]*CODE_LENGTH
    g_used = [False]*CODE_LENGTH
    for i in range(CODE_LENGTH):
        if s[i] == g[i]:
            s_used[i] = g_used[i] = True
    partial = 0
    for i in range(CODE_LENGTH):
        if not g_used[i]:
            for j in range(CODE_LENGTH):
                if not s_used[j] and g[i] == s[j]:
                    s_used[j] = True
                    partial += 1
                    break
    return (exact, partial)

class QNet(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )

    def forward(self, x):
        return self.fc(x)

class DRLMastermindAgent:
    def __init__(self, epsilon=0.2):
        self.actions = ALL_CODES
        self.model = QNet(input_size=len(self.actions)*2, output_size=len(self.actions))
        self.epsilon = epsilon

    def state_vector(self, history):
        vec = np.zeros(len(self.actions)*2)
        for guess, (e, p) in history:
            gi = CODE_INDEX[guess]
            vec[gi] = e
            vec[len(self.actions)+gi] = p
        return vec

    def choose(self, history):
        state = torch.tensor([self.state_vector(history)], dtype=torch.float32)
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        with torch.no_grad():
            qvals = self.model(state)
        return self.actions[qvals.argmax().item()]

    def update(self, guess, feedback):
        pass  # For testing only. Training logic lives elsewhere.