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

from drl_solver import DRLMastermindAgent, feedback
from retro_mastermind import create_game
import torch


def run_drl_battle(difficulty="easy"):
    game = create_game(difficulty)
    code_id = f"{len(game.colors)}c_{game.code_length}l"
    model_path = f"trained_drl_{code_id}.pth"
    print(model_path)

    agent = DRLMastermindAgent(epsilon=0.0)
    try:
        import torch

        checkpoint = torch.load(model_path)
        colors = checkpoint["colors"]
        code_length = checkpoint["code_length"]
        agent = DRLMastermindAgent(colors=colors, code_length=code_length, epsilon=0.0)
        agent.model.load_state_dict(checkpoint["state_dict"])
        #agent.model.load_state_dict(torch.load(model_path))
        print(f"✅ Loaded model: {model_path}")
    except FileNotFoundError:
        print(f"❌ Model not found for {difficulty} ({model_path}). Please train it first.")
        return

    history = []

    print(f"\n🤖 DRL AI vs Retro Mastermind — Difficulty: {difficulty.capitalize()}")
    print(f"Secret code: {game.reveal_code()}")

    while not game.is_over():
        guess = agent.choose(history)
        result = game.guess(guess)
        fb = (result["exact"], result["partial"])
        history.append((guess, fb))

        print(f"Attempt {game.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if fb[0] == game.code_length:
            print(f"🏆 DRL Solver cracked it in {game.attempts} attempts!")
            break

    if not game.is_won():
        print(f"💥 DRL AI failed. Secret was: {' '.join(game.reveal_code())}")

if __name__ == "__main__":
    run_drl_battle("medium")  # Change difficulty here


