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

import os
import json
from itertools import product
from collections import Counter
import random
import hashlib



class LearningMastermindAI:

    def __init__(self, code_length=4, colors="RGBYOP", data_file=None):
        self.code_length = code_length
        self.colors = colors
        self.data_file = data_file or self._generate_filename()
        self.knowledge = {}
        self.history = []
        self._load_data()

    def _feedback_original(self, secret, guess):
        s, g = list(secret), list(guess)
        exact = sum(a == b for a, b in zip(s, g))
        for i in range(len(s)):
            if s[i] == g[i]:
                s[i] = g[i] = None
        partial = sum(1 for c in g if c and c in s and s.remove(c))
        return (exact, partial)

    def _feedback(self, secret, guess):
        guess = list(guess)
        secret = list(secret)
        exact = 0
        partial = 0

        for i in range(len(secret)):
            if guess[i] == secret[i]:
                exact += 1
                guess[i] = secret[i] = None

        for i in range(len(guess)):
            if guess[i] and guess[i] in secret:
                partial += 1
                secret[secret.index(guess[i])] = None

        return (exact, partial)

    def _generate_filename(self):
        key = f"{self.code_length}:{self.colors}"
        hash_id = hashlib.md5(key.encode()).hexdigest()[:6]
        return f"learning_data_{hash_id}.json"


    def _load_data(self):
        if os.path.exists(self.data_file):
            print(f"📂 Loading training data from {self.data_file}...")
            with open(self.data_file, "r") as f:
                self.knowledge = json.load(f)

    def _save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.knowledge, f)

    def train(self, num_samples=5000):
        print(f"🔁 Training on {num_samples} simulated codes...")
        pool = [''.join(p) for p in product(self.colors, repeat=self.code_length)]
        for secret in pool[:num_samples]:
            for guess in pool:
                fb = self._feedback(secret, guess)
                key = f"{guess}|{fb[0]}-{fb[1]}"
                if key not in self.knowledge:
                    self.knowledge[key] = []
                self.knowledge[key].append(secret)
        self._save_data()
        print("✅ Training complete. Knowledge saved to", self.data_file)

    def choose_guess(self, remaining_pool):
        if not self.knowledge:
            return remaining_pool[0]

        scores = {}
        for guess in remaining_pool:
            total = 0
            for code in remaining_pool:
                fb = self._feedback(code, guess)
                key = f"{guess}|{fb[0]}-{fb[1]}"
                total += len(self.knowledge.get(key, []))
            scores[guess] = total

        #if not scores:
        #    print("⚠️ No viable guesses remain—defaulting to fallback.")
        #    print(f"[AI] Evaluating {len(remaining_pool)} possible guesses...")
        #    return remaining_pool[0] if remaining_pool else "R" * self.code_length
        
        #if not scores:
        #    print("⚠️ No viable guesses remain. AI will guess randomly from full space.")
        #    return ''.join(self.colors[0] for _ in range(self.code_length))

        if not scores:
            print("⚠️ No viable guesses remain. Resetting pool to all legal combinations.")
            pool = [''.join(p) for p in product(self.colors, repeat=self.code_length)]
            return random.choice(pool)

        return min(scores, key=scores.get)


    def update_history(self, guess, feedback):
        self.history.append((guess, feedback))