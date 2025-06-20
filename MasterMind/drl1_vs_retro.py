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

from drl_solver import DRLMastermindAgent, feedback, ALL_CODES
from retro_mastermind import create_game

def run_drl_battle():
    game = create_game(code_length=3, colors="RGB")
    agent = DRLMastermindAgent(epsilon=0.0)  # deterministic after training
    history = []

    print(f"\n🤖 DRL AI vs Retro Mastermind")
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
        print(f"💥 DRL AI failed. Secret was: {game.reveal_code()}")

if __name__ == "__main__":
    run_drl_battle()