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

from csp_solver import CSPConstraintSolver
from retro_mastermind import create_game

def run_csp_battle(difficulty="medium"):
    game = create_game(difficulty=difficulty)
    solver = CSPConstraintSolver(code_length=game.code_length, colors=game.colors)

    print(f"\n🧠 CSP Solver vs Retro Mastermind ({difficulty})")
    print(f"Code length: {game.code_length} | Colors: {game.colors}\n")

    while not game.is_over():
        guess = solver.next_guess()
        if not guess:
            print("❌ No valid guess satisfies all constraints.")
            break

        result = game.guess(guess)
        feedback = (result["exact"], result["partial"])
        solver.update(guess, feedback)

        print(f"Attempt {game.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if feedback[0] == game.code_length:
            print(f"🏆 CSP Solver cracked the code in {game.attempts} attempts!")
            break

    if not game.is_won():
        print(f"💥 CSP Solver failed. Code was: {' '.join(game.reveal_code())}")

if __name__ == "__main__":
    run_csp_battle()