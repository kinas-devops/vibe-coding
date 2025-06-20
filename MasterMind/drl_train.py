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
from drl_solver import DRLMastermindAgent, feedback
from retro_mastermind import DIFFICULTY_LEVELS
import numpy as np
import torch

def simulate_episode(agent, code, training=True):
    history = []
    state = agent.state_vector(history)
    total_reward = 0
    max_steps = 10

    for step in range(max_steps):
        guess = agent.choose(history, training=training)
        fb = feedback(code, guess)

        reward = 0.2 * fb[0] + 0.1 * fb[1]
        if guess in [g for g, _ in history]:
            reward -= 0.6
        else:
            reward += 0.05
        if fb[0] == len(code):
            reward = 1.0
        done = fb[0] == len(code)

        new_history = history + [(guess, fb)]
        next_state = agent.state_vector(new_history)
        agent.store(state, guess, reward, next_state, done)

        state = next_state
        history = new_history
        total_reward += reward

        if done:
            break

    return step + 1 if done else max_steps

def train_agent(episodes=3000, difficulty="easy", update_target_every=10):
    config = DIFFICULTY_LEVELS[difficulty]
    COLORS = config["colors"]
    CODE_LENGTH = config["code_length"]
    code_id = f"{len(COLORS)}c_{CODE_LENGTH}l"

    agent = DRLMastermindAgent(colors=COLORS, code_length=CODE_LENGTH, epsilon=1.0)
    attempts_list = []

    for ep in range(1, episodes + 1):
        code = ''.join(np.random.choice(list(COLORS), size=CODE_LENGTH))
        attempts = simulate_episode(agent, code)
        agent.train_step()
        agent.epsilon = max(agent.epsilon * 0.995, 0.05)

        if ep % update_target_every == 0:
            agent.update_target()
        attempts_list.append(attempts)

        if ep % 100 == 0:
            avg = np.mean(attempts_list[-100:])
            print(f"Episode {ep:>4} | Avg Attempts (last 100): {avg:.2f} | Epsilon: {agent.epsilon:.3f}")

    torch.save({
        "colors": COLORS,
        "code_length": CODE_LENGTH,
        "state_dict": agent.model.state_dict()
    }, f"trained_drl_{code_id}.pth")
    print(f"\n✅ Saved model: trained_drl_{code_id}.pth")

    # Plot progress
    window = 100
    smoothed = [np.mean(attempts_list[max(0, i - window):i]) for i in range(1, len(attempts_list)+1)]
    plt.plot(smoothed)
    plt.title(f"Training Progress ({difficulty.capitalize()})")
    plt.xlabel("Episode")
    plt.ylabel("Average Attempts")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return agent

if __name__ == "__main__":
    train_agent(episodes=12000, difficulty="medium")