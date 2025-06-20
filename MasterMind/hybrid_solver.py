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
from itertools import product
from entropy_solver import EntropySolver  # Make sure you have this file in the same directory!

class HybridSolver:
    def __init__(self, code_length=4, colors="RGBYOP", population_size=80, mutation_rate=0.1, switch_at=7):
        self.code_length = code_length
        self.colors = colors
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.switch_at = switch_at

        self.pool = self._generate_all_codes()
        self.population = random.choices(self.pool, k=self.population_size)
        self.history = []
        self.entropy_solver = EntropySolver(code_length=code_length, colors=colors)
        self.attempts = 0
        self.switched = False

    def _generate_all_codes(self):
        return [''.join(p) for p in product(self.colors, repeat=self.code_length)]

    def _feedback(self, secret, guess):
        s, g = list(secret), list(guess)
        exact = 0
        partial = 0
        for i in range(self.code_length):
            if s[i] == g[i]:
                exact += 1
                s[i] = g[i] = None
        for i in range(self.code_length):
            if g[i] and g[i] in s:
                partial += 1
                s[s.index(g[i])] = None
        return (exact, partial)

    def _score(self, guess):
        return sum(1 for past_guess, fb in self.history if self._feedback(guess, past_guess) == fb)

    def _breed(self, parent1, parent2):
        cut = random.randint(1, self.code_length - 1)
        child = parent1[:cut] + parent2[cut:]
        return self._mutate(child)

    def _mutate(self, code):
        code = list(code)
        for i in range(self.code_length):
            if random.random() < self.mutation_rate:
                code[i] = random.choice(self.colors)
        return ''.join(code)

    def next_guess(self):
        if self.switched:
            return self.entropy_solver.next_guess()

        if self.attempts >= self.switch_at:
            print("🔁 Switching to entropy fallback...")
            self.switched = True
            for guess, fb in self.history:
                self.entropy_solver.update(guess, fb)
            return self.entropy_solver.next_guess()

        # Genetic phase
        scored = sorted(self.population, key=self._score, reverse=True)
        top = scored[:self.population_size // 5]
        new_population = top[:]
        while len(new_population) < self.population_size:
            parents = random.sample(top, 2)
            child = self._breed(parents[0], parents[1])
            new_population.append(child)
        self.population = new_population

        guess = scored[0]
        self.attempts += 1
        return guess

    def update(self, guess, feedback):
        self.history.append((guess, feedback))
        if self.switched:
            self.entropy_solver.update(guess, feedback)
            