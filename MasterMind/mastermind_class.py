import random

class Mastermind:
    def __init__(self, code_length=4, colors="RGBYOP", max_attempts=10):
        self.colors = colors
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.secret_code = self._generate_code()
        self.attempts = 0
        self.history = []

    def _generate_code(self):
        return [random.choice(self.colors) for _ in range(self.code_length)]

    def guess(self, guess_code):
        if len(guess_code) != self.code_length:
            raise ValueError(f"Guess must be {self.code_length} characters long.")
        self.attempts += 1
        guess_code = guess_code.upper()
        result = self._evaluate_guess(guess_code)
        self.history.append((guess_code, result))
        return result

    def _evaluate_guess(self, guess):
        exact = sum(a == b for a, b in zip(guess, self.secret_code))
        # Count correct colors in wrong positions
        secret_temp = list(self.secret_code)
        guess_temp = list(guess)
        for i in range(len(guess)):
            if guess[i] == self.secret_code[i]:
                secret_temp[i] = guess_temp[i] = None
        partial = sum(guess_temp.count(c) for c in secret_temp if c and guess_temp.count(c))
        return {"exact": exact, "partial": partial}

    def is_won(self):
        return any(result['exact'] == self.code_length for _, result in self.history)

    def is_over(self):
        return self.attempts >= self.max_attempts or self.is_won()

    def reveal_code(self):
        return ''.join(self.secret_code)