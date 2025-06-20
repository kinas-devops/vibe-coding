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

class KnuthSolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = colors
        self.attempts = 0
        self.guess_history = []
        self.pool = self._generate_possibilities()

    def _generate_possibilities(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, secret, guess):
        secret = list(secret)
        guess = list(guess)
        exact = 0
        partial = 0

        for i in range(len(secret)):
            if guess[i] == secret[i]:
                exact += 1
                secret[i] = guess[i] = None

        for i in range(len(secret)):
            if guess[i] and guess[i] in secret:
                partial += 1
                secret[secret.index(guess[i])] = None

        return (exact, partial)

    def next_guess(self):
        if self.attempts == 0:
            return self._starting_guess()
        return self.pool[0]  # Simplified (optimal choice logic can be added here)

    def _starting_guess(self):
        # Generic starting guess for any size (alternating first two colors)
        colors = [self.colors[0], self.colors[1]]
        return ''.join(colors[i % 2] for i in range(self.code_length))

    def register_feedback(self, guess, feedback):
        self.attempts += 1
        self.guess_history.append((guess, feedback))
        self.pool = [
            code for code in self.pool
            if self._feedback(code, guess) == feedback
        ]