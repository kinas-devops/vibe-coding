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

from knuth_solver import KnuthSolver
from retro_mastermind import create_game

def run_knuth_battle(difficulty="medium"):
    game = create_game(difficulty=difficulty)
    solver = KnuthSolver(code_length=game.code_length, colors=game.colors)

    print(f"\n🎮 Difficulty: {difficulty.capitalize()} | Code length: {game.code_length} | Colors: {game.colors}")
    print(f"🧠 Knuth's Solver is attempting to break the code...\n")

    while not game.is_over():
        guess = solver.next_guess()
        result = game.guess(guess)
        solver.register_feedback(guess, (result["exact"], result["partial"]))

        print(f"Attempt {solver.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if result["exact"] == game.code_length:
            print(f"🏆 Code cracked in {solver.attempts} guesses: {guess}")
            break

    if not game.is_won():
        print(f"\n❌ AI failed. Secret was: {game.reveal_code()}")

if __name__ == "__main__":
    run_knuth_battle("medium")  # Change to 'easy' or 'hard' as desired