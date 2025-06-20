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

from pysat.formula import IDPool
from pysat.solvers import Glucose3
from itertools import product, permutations

class CSPSolver:
    def __init__(self, code_length=4, colors="RGBYOP"):
        self.code_length = code_length
        self.colors = colors
        self.color_list = list(colors)
        self.vpool = IDPool()
        self.guesses = []
        self.feedbacks = []

    def var(self, pos, color):
        return self.vpool.id(f"P{pos}_{color}")

    def build_base_constraints(self, solver):
        for pos in range(self.code_length):
            literals = [self.var(pos, c) for c in self.colors]
            # One color per position
            solver.add_clause(literals)
            # At most one
            for i in range(len(literals)):
                for j in range(i + 1, len(literals)):
                    solver.add_clause([-literals[i], -literals[j]])

    def encode_feedback(self, solver, guess, feedback):
        possible_codes = []
        all_colors = list(product(self.color_list, repeat=self.code_length))
        for candidate in all_colors:
            exact = sum(c1 == c2 for c1, c2 in zip(candidate, guess))
            used = [False]*self.code_length
            partial = 0
            for i in range(self.code_length):
                if candidate[i] == guess[i]:
                    used[i] = True
            for i in range(self.code_length):
                if candidate[i] != guess[i]:
                    for j in range(self.code_length):
                        if not used[j] and guess[i] == candidate[j] and guess[j] != candidate[j]:
                            used[j] = True
                            partial += 1
                            break
            if (exact, partial) == feedback:
                possible_codes.append(candidate)

        # Encode the possible codes for this feedback
        code_clauses = []
        for code in possible_codes:
            clause = []
            for pos, color in enumerate(code):
                clause.append(self.var(pos, color))
            code_clauses.append(clause)
        solver.append_formula(code_clauses, no_return=True)

    def next_guess(self):
        solver = Glucose3()
        self.build_base_constraints(solver)
        for guess, fb in zip(self.guesses, self.feedbacks):
            self.encode_feedback(solver, guess, fb)

        if solver.solve():
            model = solver.get_model()
            decoded = ['?' for _ in range(self.code_length)]
            for pos in range(self.code_length):
                for color in self.colors:
                    if self.var(pos, color) in model:
                        decoded[pos] = color
            return ''.join(decoded)
        return None

    def update(self, guess, feedback):
        self.guesses.append(guess)
        self.feedbacks.append(feedback)
        