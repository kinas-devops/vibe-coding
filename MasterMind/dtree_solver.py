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

class DecisionTreeSolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = colors
        self.history = []
        self.possible = self._generate_all_codes()
        self.all_guesses = self.possible[:]

    def _generate_all_codes(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, secret, guess):
        exact = sum(s == g for s, g in zip(secret, guess))
        s_unused = [s for s, g in zip(secret, guess) if s != g]
        g_unused = [g for s, g in zip(secret, guess) if s != g]
        partial = 0
        for c in set(g_unused):
            partial += min(s_unused.count(c), g_unused.count(c))
        return (exact, partial)

    def _partition_codes(self, guess, pool):
        buckets = defaultdict(list)
        for code in pool:
            fb = self._feedback(code, guess)
            buckets[fb].append(code)
        return buckets

    def _minimax_score(self, guess, pool):
        buckets = self._partition_codes(guess, pool)
        worst = max(len(v) for v in buckets.values())
        return worst

    def _next_best_guess(self, pool):
        scores = {}
        for guess in self.all_guesses:
            scores[guess] = self._minimax_score(guess, pool)
        min_worst = min(scores.values())
        best_guesses = [g for g in scores if scores[g] == min_worst]
        for g in best_guesses:
            if g in pool:
                return g
        return best_guesses[0]

    def next_guess(self):
        if len(self.history) == 0:
            return self._next_best_guess(self.possible)
        return self._next_best_guess(self.possible)

    def update(self, guess, feedback):
        self.history.append((guess, feedback))
        self.possible = [code for code in self.possible if self._feedback(code, guess) == feedback]
        