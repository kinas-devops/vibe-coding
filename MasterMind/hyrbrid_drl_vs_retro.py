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

from hybrid_drl_solver import HybridDRLCSPSolver
from retro_mastermind import create_game

def run_hybrid_drl_battle(difficulty="medium"):
    game = create_game(difficulty=difficulty)
    code_id = f"{len(game.colors)}c_{game.code_length}l"
    model_path = f"trained_drl_{code_id}.pth"

    solver = HybridDRLCSPSolver(code_length=game.code_length, colors=game.colors, model_path=model_path)

    print(f"\n🧠 Hybrid DRL+CSP Solver vs Retro Mastermind ({difficulty.capitalize()})")
    print(f"Secret code: {game.reveal_code()}")

    while not game.is_over():
        guess = solver.next_guess()
        if not guess:
            print("❌ No consistent guess found. Aborting.")
            break

        result = game.guess(guess)
        fb = (result["exact"], result["partial"])
        solver.update(guess, fb)

        print(f"Attempt {game.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if fb[0] == game.code_length:
            print(f"🏆 Hybrid DRL+CSP Solver cracked the code in {game.attempts} attempts!")
            break

    if not game.is_won():
        print(f"💥 Solver failed. Secret was: {' '.join(game.reveal_code())}")

if __name__ == "__main__":
    run_hybrid_drl_battle("medium")  # change to "easy" or "hard" as needed