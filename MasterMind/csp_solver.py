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

from constraint import Problem, ExactSumConstraint
from itertools import product

class CSPConstraintSolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = list(colors)
        self.domains = list(product(self.colors, repeat=self.code_length))
        self.previous_constraints = []

    def _feedback(self, secret, guess):
        exact = sum(s == g for s, g in zip(secret, guess))
        secret_unused = [s for s, g in zip(secret, guess) if s != g]
        guess_unused = [g for s, g in zip(secret, guess) if s != g]
        partial = 0
        for c in set(guess_unused):
            partial += min(secret_unused.count(c), guess_unused.count(c))
        return exact, partial

    def update(self, guess, feedback):
        self.previous_constraints.append((guess, feedback))

    def next_guess(self):
        for candidate in self.domains:
            matches = all(self._feedback(candidate, g) == fb for g, fb in self.previous_constraints)
            if matches:
                return ''.join(candidate)
        return None  # No consistent code found