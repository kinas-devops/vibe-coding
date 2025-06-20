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

from itertools import product
from collections import defaultdict
import math
import matplotlib.pyplot as plt

class EntropySolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = colors
        self.pool = self._generate_pool()
        self.all_guesses = self.pool[:]
        self.attempts = 0
        self.guess_history = []

    def _generate_pool(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, code, guess):
        code = list(code)
        guess = list(guess)
        exact = 0
        partial = 0

        for i in range(len(code)):
            if code[i] == guess[i]:
                exact += 1
                code[i] = guess[i] = None
        for i in range(len(guess)):
            if guess[i] and guess[i] in code:
                partial += 1
                code[code.index(guess[i])] = None
        return (exact, partial)

    def next_guess(self):
        entropy_scores = {}
        for guess in self.all_guesses:
            outcome_counts = defaultdict(int)
            for code in self.pool:
                fb = self._feedback(code, guess)
                outcome_counts[fb] += 1
            total = sum(outcome_counts.values())
            entropy = -sum((count/total) * math.log2(count/total) for count in outcome_counts.values())
            entropy_scores[guess] = entropy



        # 🔥 Print top 10 guesses and entropy
        print("\n📊 Entropy scores (top 10):")
        for g, e in sorted(entropy_scores.items(), key=lambda x: -x[1])[:10]:
            print(f"  {g} → {e:.3f} bits")


        max_entropy = max(entropy_scores.values())
        best_guesses = [g for g, e in entropy_scores.items() if e == max_entropy]
        for g in best_guesses:
            if g in self.pool:
                return g


        # Optional: inside the method before returning best guess
        guesses = list(entropy_scores.keys())
        values = [entropy_scores[g] for g in guesses]

        plt.figure(figsize=(10, 4))
        plt.bar(range(len(values)), values, tick_label=guesses)
        plt.xticks(rotation=90)
        plt.title("Entropy per Guess (bits)")
        plt.ylabel("Information Gain")
        plt.tight_layout()
        plt.show()

        return best_guesses[0]

    def update(self, guess, feedback):
        self.attempts += 1
        self.guess_history.append((guess, feedback))
        self.pool = [code for code in self.pool if self._feedback(code, guess) == feedback]