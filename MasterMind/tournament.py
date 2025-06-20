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

import random
from retro_mastermind import Mastermind, DIFFICULTY_LEVELS
from knuth_solver import KnuthSolver
from entropy_solver import EntropySolver
from genetic_solver import GeneticSolver
from hybrid_solver import HybridSolver

AI_CLASSES = {
    "Knuth": KnuthSolver,
    "Entropy": EntropySolver,
    "Genetic": GeneticSolver,
    "Hybrid": HybridSolver
}

def run_match(ai_name, AIClass, secret_code, config):
    game = Mastermind(**config)
    game.secret_code = list(secret_code)
    solver = AIClass(code_length=len(secret_code), colors=config["colors"])

    attempts = 0
    while not game.is_over():
        guess = solver.next_guess()
        result = game.guess(guess)
        feedback = (result["exact"], result["partial"])
        if hasattr(solver, "update"):
            solver.update(guess, feedback)
        elif hasattr(solver, "register_feedback"):
            solver.register_feedback(guess, feedback)
        attempts += 1
        if result["exact"] == len(secret_code):
            return attempts
    return None  # Failed to solve

def tournament(runs=10, difficulty="medium", seed=42):
    print(f"\n🎮 Mastermind AI Tournament — Difficulty: {difficulty}, Rounds: {runs}")
    config = DIFFICULTY_LEVELS[difficulty]
    code_length = config["code_length"]
    colors = config["colors"]
    random.seed(seed)

    results = {name: [] for name in AI_CLASSES}

    for match in range(1, runs + 1):
        secret = ''.join(random.choices(colors, k=code_length))
        print(f"\n🔒 Round {match}: Secret = {secret}")

        for name, AIClass in AI_CLASSES.items():
            attempts = run_match(name, AIClass, secret, config)
            results[name].append(attempts if attempts is not None else float('inf'))
            status = f"{attempts} tries" if attempts else "❌ Failed"
            print(f"  {name:<8} → {status}")

    # Final results
    print("\n🏁 Final Results:")
    for name, scores in results.items():
        avg = sum(s for s in scores if s != float('inf')) / len(scores)
        fails = scores.count(float('inf'))
        print(f"  {name:<8} — Avg Attempts: {avg:.2f}, Failures: {fails}/{runs}")


if __name__ == "__main__":
    tournament(runs=20, difficulty="medium")