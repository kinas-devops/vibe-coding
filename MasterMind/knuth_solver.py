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
        self.pool = self._generate_pool()
        self.possible_guesses = self.pool[:]
        self.attempts = 0
        self.guess_history = []

    def _generate_pool(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, secret, guess):
        s = list(secret)
        g = list(guess)
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

        minmax_scores = {}
        for guess in self.possible_guesses:
            score_counts = defaultdict(int)
            for code in self.pool:
                fb = self._feedback(code, guess)
                score_counts[fb] += 1
            worst_case = max(score_counts.values())
            minmax_scores[guess] = worst_case

        # Find smallest worst case score (minimax)
        min_score = min(minmax_scores.values())
        best_guesses = [k for k, v in minmax_scores.items() if v == min_score]

        # Prefer guesses still in pool
        for g in best_guesses:
            if g in self.pool:
                return g
        return best_guesses[0]

    def _starting_guess(self):
        if len(self.colors) >= 2:
            base = [self.colors[0], self.colors[1]]
            return ''.join(base[i % 2] for i in range(self.code_length))
        return self.pool[0]

    def register_feedback(self, guess, feedback):
        self.attempts += 1
        self.guess_history.append((guess, feedback))
        self.pool = [code for code in self.pool if self._feedback(code, guess) == feedback]