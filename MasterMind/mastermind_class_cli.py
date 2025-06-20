import random
from colorama import Fore, Style, init

COLOR_MAP = {
    'R': Fore.RED,
    'G': Fore.GREEN,
    'B': Fore.BLUE,
    'Y': Fore.YELLOW,
    'O': Fore.MAGENTA,
    'P': Fore.CYAN
}

DIFFICULTY_LEVELS = {
    'easy': {'code_length': 3, 'colors': 'RGB', 'max_attempts': 12},
    'medium': {'code_length': 4, 'colors': 'RGBYOP', 'max_attempts': 10},
    'hard': {'code_length': 5, 'colors': 'RGBYOPCM', 'max_attempts': 8}
}

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
        guess = list(guess)
        secret = self.secret_code.copy()
        exact = 0
        partial = 0

        # First pass: count exact matches
        for i in range(len(secret)):
            if guess[i] == secret[i]:
                exact += 1
                guess[i] = None
                secret[i] = None

        # Second pass: count partial matches
        for i in range(len(guess)):
            if guess[i] and guess[i] in secret:
                partial += 1
                secret[secret.index(guess[i])] = None

        return {"exact": exact, "partial": partial}

    def is_won(self):
        return any(result['exact'] == self.code_length for _, result in self.history)

    def is_over(self):
        return self.attempts >= self.max_attempts or self.is_won()

    def reveal_code(self):
        return ''.join(self.secret_code)


def colorize(char):
    return COLOR_MAP.get(char.upper(), '') + char + Style.RESET_ALL

    
def play():
    print("Welcome to Mastermind!")

    print("Choose difficulty: easy, medium, hard")
    choice = input("> ").lower()
    config = DIFFICULTY_LEVELS.get(choice, DIFFICULTY_LEVELS['medium'])

    #game = Mastermind()
    game = Mastermind(**config)

    print(f"Colors: {game.colors}")
    print(f"Guess the {game.code_length}-character code. You have {game.max_attempts} attempts.")

    while not game.is_over():
        try:
            guess = input(f"\nAttempt {game.attempts + 1}: ").strip()
            result = game.guess(guess)
            colored_guess = ''.join(colorize(c) for c in guess)
            print(f"You guessed: {colored_guess}")
            print(f"Exact matches: {result['exact']}, Partial matches: {result['partial']}")
        except ValueError as ve:
            print(f"Error: {ve}")

    if game.is_won():
        print("\n🎉 Congratulations! You cracked the code!")
    else:
        print(f"\n💥 Game over. The code was: {game.reveal_code()}")

if __name__ == "__main__":
    init(autoreset=True)
    play()