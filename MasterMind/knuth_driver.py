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

from retro_mastermind import create_game

game = create_game(difficulty="medium")

print(f"\nAI is trying to crack the code: {game.code_length} pegs, using colors: {game.colors}")

from itertools import product
pool = product(game.colors, repeat=game.code_length)

for i, guess_tuple in enumerate(pool, 1):
    guess = ''.join(guess_tuple)
    result = game.guess(guess)
    print(f"\nAttempt {i}:")
    print(game.format_guess_feedback(guess, result))

    if result['exact'] == game.code_length:
        print(f"\n🎉 AI cracked the code in {i} guesses!")
        break

if not game.is_won():
    print(f"\n💥 AI failed. Secret code was: {game.reveal_code()}")