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

from genetic_solver import GeneticSolver
from retro_mastermind import create_game

def run_genetic_battle(difficulty="medium"):
    game = create_game(difficulty=difficulty)
    solver = GeneticSolver(code_length=game.code_length, colors=game.colors)

    print(f"\n🎮 Genetic AI vs Retro Mastermind (Difficulty: {difficulty})")
    print(f"Code length: {game.code_length} | Colors: {game.colors}\n")

    while not game.is_over():
        guess = solver.next_guess()
        result = game.guess(guess)
        solver.update(guess, (result["exact"], result["partial"]))

        print(f"Attempt {solver.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if result["exact"] == game.code_length:
            print(f"🏆 Genetic AI cracked the code in {solver.attempts} attempts!")
            break

    if not game.is_won():
        print(f"💥 AI failed. Secret code was: {' '.join(game.reveal_code())}")

if __name__ == "__main__":
    run_genetic_battle()