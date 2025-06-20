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

import matplotlib.pyplot as plt
from drl_solver import DRLMastermindAgent, feedback, ALL_CODES
from retro_mastermind import DIFFICULTY_LEVELS
from itertools import product
import numpy as np
import torch


def simulate_episode(agent, secret_code):
    history = []
    total_reward = 0
    state = agent.state_vector(history)
    max_steps = 10

    for step in range(max_steps):
        guess = agent.choose(history, training=True)
        fb = feedback(secret_code, guess)
        reward = 1.0 if fb[0] == len(secret_code) else -0.1
        done = fb[0] == len(secret_code)

        new_history = history + [(guess, fb)]
        next_state = agent.state_vector(new_history)

        agent.store(state, guess, reward, next_state, done)
        state = next_state
        history = new_history
        total_reward += reward

        if done:
            break
    return step + 1 if done else max_steps


def train_agent(episodes=1000, difficulty="easy", update_target_every=10):
    config = DIFFICULTY_LEVELS[difficulty]
    COLORS = config["colors"]
    CODE_LENGTH = config["code_length"]

    #agent = DRLMastermindAgent()
    agent = DRLMastermindAgent(colors=COLORS, code_length=CODE_LENGTH)
    attempts_list = []

    for ep in range(1, episodes + 1):
        #code = ''.join(np.random.choice(list("RGB"), size=3))
        code = ''.join(np.random.choice(list(COLORS), size=CODE_LENGTH))
        attempts = simulate_episode(agent, code)
        agent.train_step()
        if ep % update_target_every == 0:
            agent.update_target()
        attempts_list.append(attempts)

        if ep % 100 == 0:
            avg = np.mean(attempts_list[-100:])
            print(f"Episode {ep} | Avg Attempts (last 100): {avg:.2f}")

    code_id = f"{len(COLORS)}c_{CODE_LENGTH}l"
    meta = {
        "colors": COLORS,
        "code_length": CODE_LENGTH,
        "state_dict": agent.model.state_dict()
    }
    torch.save(meta, f"trained_drl_{code_id}.pth")
    #torch.save(agent.model.state_dict(), f"trained_drl_{code_id}.pth")
    #torch.save(agent.model.state_dict(), "trained_drl.pth")

    # Plotting results
    window = 50
    smoothed = [np.mean(attempts_list[i-window:i]) if i > window else np.mean(attempts_list[:i]) for i in range(1, len(attempts_list))]
    plt.plot(smoothed)
    plt.title("Training Progress: Attempts per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Attempts")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return agent


if __name__ == "__main__":
    train_agent(episodes=2000,difficulty="hard")
