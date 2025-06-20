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

def simulate_episode(agent, code):
    history = []
    state = agent.state_vector(history)
    max_steps = 10

    for step in range(max_steps):
        guess = agent.choose(history, training=True)
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

        if done:
            break

    return step + 1 if done else max_steps

def train_difficulty(agent, difficulty, episodes=3000, update_target_every=10):
    config = DIFFICULTY_LEVELS[difficulty]
    COLORS = config["colors"]
    CODE_LENGTH = config["code_length"]
    code_id = f"{len(COLORS)}c_{CODE_LENGTH}l"

    # Update agent with new environment
    agent.colors = COLORS
    agent.code_length = CODE_LENGTH
    agent.actions = [''.join(p) for p in __import__('itertools').product(COLORS, repeat=CODE_LENGTH)]
    agent.index = {code: i for i, code in enumerate(agent.actions)}
    agent.model = agent.__class__.model.__func__(agent)
    agent.target = agent.__class__.model.__func__(agent)
    agent.update_target()

    print(f"\n🎯 Training on difficulty: {difficulty} | Color set: {COLORS} | Code length: {CODE_LENGTH}")
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
            print(f"  Episode {ep:>4} | Avg Attempts (last 100): {avg:.2f} | Epsilon: {agent.epsilon:.3f}")

    torch.save({
        "colors": COLORS,
        "code_length": CODE_LENGTH,
        "state_dict": agent.model.state_dict()
    }, f"trained_drl_{code_id}.pth")

    return attempts_list

def train_curriculum(curriculum=["easy", "medium", "hard"], episodes=3000):
    all_results = {}
    agent = DRLMastermindAgent(epsilon=1.0)

    for diff in curriculum:
        scores = train_difficulty(agent, difficulty=diff, episodes=episodes)
        all_results[diff] = scores

    # 📊 Plotting all curves
    window = 100
    plt.figure(figsize=(10, 5))
    for diff, attempts in all_results.items():
        smoothed = [np.mean(attempts[max(0, i - window):i]) for i in range(1, len(attempts) + 1)]
        plt.plot(smoothed, label=diff.capitalize())

    plt.title("DRL Curriculum Training Progress")
    plt.xlabel("Episode")
    plt.ylabel("Average Attempts")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train_curriculum(episodes=3000)