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

import itertools
import statistics
import webbrowser
from retro_mastermind import create_game



# Define a function to calculate the feedback for a given guess
def calculate_feedback(guess, solution):
    """Calculate the feedback for a given guess."""
    black_pegs = 0
    white_pegs = 0
    # Create copies of the lists to avoid modifying the originals
    temp_guess = list(guess)
    temp_solution = list(solution)
    # Count the black pegs (correct color and position)
    for i in range(NUM_PINS):
        if temp_guess[i] == temp_solution[i]:
            black_pegs += 1
            # Mark the peg as used with a special value
            temp_guess[i] = -1
            temp_solution[i] = -1
    # Count the white pegs (correct color, incorrect position)
    for i in range(NUM_PINS):
        if temp_guess[i] != -1 and temp_guess[i] in temp_solution:
            white_pegs += 1
            # Mark the peg as used with a special value
            j = temp_solution.index(temp_guess[i])
            temp_solution[j] = -1
    # Return the feedback as a tuple
    return (black_pegs, white_pegs)


def solve_mastermind():
    """Solve Mastermind puzzles using the Knuth five-guess algorithm."""

    # Generate all possible 4-color combinations
    #possibilities = list(itertools.product(range(1, NUM_COLORS + 1), repeat=NUM_PINS))
    possibilities = list(itertools.product(game.colors, repeat=game.code_length))
    print(possibilities)
    # Initialize the number of attempts
    attempts = 0
    # Initialize the first guess as 1122
    #guess = [1, 1, 2, 2]
    guess = "RRGG"
    # Loop until the solution is found
    while True:
        # Increment the number of attempts
        attempts += 1
        # Show the current guess
        print(f"Attempt {attempts}: {guess}")
        # Get the feedback for the current guess

        #feedback_result = get_feedback()
        # guess = ''.join(guess_tuple)
        result = game.guess(guess)
        feedback_result= game.guess(guess)
        #print(f"\nAttempt {i}:")
        print(game.format_guess_feedback(guess, result))

        print(f"Attempt {attempts}: {guess}, Feedback: {feedback_result}")
        # Check if the guess is equal to the solution
        if feedback_result == (NUM_PINS, 0):
            # Congratulations and end the loop
            print("Congratulations, you solved the Mastermind puzzle!")
            break
        # Filter the possibilities using the feedback
        possibilities = [p for p in possibilities if calculate_feedback(guess, p) == feedback_result]
        # Choose the next guess using the minimax technique
        if not possibilities:
            print("Error: No remaining possibilities. Check the feedback provided.")
            break
        best_guess = None
        best_score = float('inf')
        # For each possibility in the remaining possibilities
        for p in possibilities:
            # Count the number of possibilities that would be eliminated for each feedback
            feedback_counts = {}
            for q in possibilities:
                f = calculate_feedback(p, q)
                feedback_counts[f] = feedback_counts.get(f, 0) + 1
            # The worst case is the feedback that eliminates the least possibilities
            worst_score = max(feedback_counts.values()) if feedback_counts else 0
            # Choose the guess that has the best worst case
            if worst_score < best_score:
                best_guess = p
                best_score = worst_score
        # Assign the best guess to the current guess
        guess = best_guess






        if result['exact'] == game.code_length:
            print(f"\n🎉 AI cracked the code in {i} guesses!")
            break

    if not game.is_won():
        print(f"\n💥 AI failed. Secret code was: {game.reveal_code()}")

    return attempts


if __name__ == "__main__":
    game = create_game(difficulty="medium")

    print(f"\nAI is trying to crack the code: {game.code_length} pegs, using colors: {game.colors}")

    # Define constants for the number of pins and colors
    NUM_PINS = game.code_length
    NUM_COLORS = len(game.colors)

    solve_mastermind()

