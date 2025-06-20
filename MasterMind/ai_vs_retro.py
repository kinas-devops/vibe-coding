# =============================================================================
# Generated with help from Microsoft AI Copilot (https://copilot.microsoft.com)
# =============================================================================

__author__ = "Kinas"
__copyright__ = "Copyright 2025, Vibe-Coding Project"
__credits__ = ["Kinas"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Kinas"
__email__ = "kinas.devops@gmail.com"
__status__ = "Production"


from learning_ai import LearningMastermindAI
from retro_mastermind import create_game
from itertools import product

def run_ai_battle(difficulty="medium", train_if_missing=True):
    ai = LearningMastermindAI()
    if not ai.knowledge and train_if_missing:
        ai.train()

    game = create_game(difficulty=difficulty)
    pool = [''.join(p) for p in product(game.colors, repeat=game.code_length)]

    print(f"\n🎮 AI vs Retro Mastermind (difficulty: {difficulty})")
    print(f"Code length: {game.code_length} | Available colors: {game.colors}\n")

    while not game.is_over():
        guess = ai.choose_guess(pool)
        result = game.guess(guess)
        ai.update_history(guess, (result["exact"], result["partial"]))
        pool = [code for code in pool if ai._feedback(code, guess) == (result["exact"], result["partial"])]

        print(f"Attempt {game.attempts}:")
        print(game.format_guess_feedback(guess, result))
        print()

        if result["exact"] == game.code_length:
            print(f"🏆 AI cracked the code in {game.attempts} attempts!")
            break

    if not game.is_won():
        print(f"💥 AI failed. Secret code was: {' '.join(game.reveal_code())}")

if __name__ == "__main__":
    run_ai_battle("hard")