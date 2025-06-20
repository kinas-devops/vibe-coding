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

class ESRSolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = colors
        self.pool = self._generate_all_codes()
        self.all_guesses = self.pool[:]
        self.history = []
        self.attempts = 0

    def _generate_all_codes(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, secret, guess):
        s, g = list(secret), list(guess)
        exact = 0
        partial = 0
        for i in range(len(s)):
            if s[i] == g[i]:
                exact += 1
                s[i] = g[i] = None
        for i in range(len(s)):
            if g[i] and g[i] in s:
                partial += 1
                s[s.index(g[i])] = None
        return (exact, partial)

    def next_guess(self):
        if self.attempts == 0:
            return self._starting_guess()

        scores = {}
        for guess in self.all_guesses:
            outcome_counts = defaultdict(int)
            for code in self.pool:
                feedback = self._feedback(code, guess)
                outcome_counts[feedback] += 1
            total = sum(outcome_counts.values())
            # 🎯 Expected Size Reduction (improved): Weighted average
            expected_remaining = sum(count * (count / total) for count in outcome_counts.values())
            scores[guess] = expected_remaining

        # 🧠 Choose guess with minimum expected pool size
        best_score = min(scores.values())
        best_guesses = [g for g in scores if scores[g] == best_score]

        for g in best_guesses:
            if g in self.pool:
                return g
        return best_guesses[0]

    def _starting_guess(self):
        if len(self.colors) >= 2:
            return ''.join(self.colors[i % 2] for i in range(self.code_length))
        return self.pool[0]

    def update(self, guess, feedback):
        self.history.append((guess, feedback))
        self.pool = [code for code in self.pool if self._feedback(code, guess) == feedback]
        self.attempts += 1