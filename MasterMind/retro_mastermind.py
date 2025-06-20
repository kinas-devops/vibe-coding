# retro_mastermind.py

import random
import os
from colorama import Fore, Style, init
init(autoreset=True)

# ─── Configuration ──────────────────────────
DIFFICULTY_LEVELS = {
    'easy': {'code_length': 3, 'colors': 'RGB', 'max_attempts': 12},
    'medium': {'code_length': 4, 'colors': 'RGBYOP', 'max_attempts': 10},
    'hard': {'code_length': 5, 'colors': 'RGBYOPCM', 'max_attempts': 8}
}

BLOCK = '█'
COLOR_MAP = {
    'R': Fore.RED,    'G': Fore.GREEN,  'B': Fore.BLUE,
    'Y': Fore.YELLOW, 'O': Fore.MAGENTA, 'P': Fore.CYAN,
    'C': Fore.LIGHTBLUE_EX, 'M': Fore.LIGHTMAGENTA_EX
}

def color_block(char):
    return COLOR_MAP.get(char.upper(), Fore.WHITE) + BLOCK + Style.RESET_ALL


# ─── Mastermind Engine ──────────────────────
class Mastermind:
    def __init__(self, code_length=4, colors="RGBYOP", max_attempts=10):
        self.colors = colors
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.secret_code = [random.choice(colors) for _ in range(code_length)]
        self.attempts = 0
        self.history = []

    def guess(self, guess_code):
        if len(guess_code) != self.code_length:
            raise ValueError(f"Guess must be {self.code_length} characters.")
        self.attempts += 1
        guess_code = guess_code.upper()
        result = self.evaluate_guess(guess_code)
        self.history.append((guess_code, result))
        return result

    def evaluate_guess(self, guess):
        guess = list(guess)
        secret = self.secret_code.copy()
        exact = 0
        partial = 0

        for i in range(len(secret)):
            if guess[i] == secret[i]:
                exact += 1
                guess[i] = None
                secret[i] = None

        for i in range(len(guess)):
            if guess[i] and guess[i] in secret:
                partial += 1
                secret[secret.index(guess[i])] = None

        return {"exact": exact, "partial": partial}

    def is_won(self):
        return any(r['exact'] == self.code_length for _, r in self.history)

    def is_over(self):
        return self.attempts >= self.max_attempts or self.is_won()

    def reveal_code(self):
        return ''.join(self.secret_code)

    def format_guess_feedback(self, guess, result):
        colored_guess = ' '.join(color_block(c) for c in guess)
        exact = f"{Fore.WHITE}●" * result['exact']
        partial = f"{Fore.LIGHTBLACK_EX}○" * result['partial']
        none = f"{Fore.BLACK}–" * (self.code_length - result['exact'] - result['partial'])

        feedback_line = f"Guess:   {colored_guess}\nFeedback: {exact}{partial}{none} {Style.RESET_ALL}"
        return feedback_line

# ─── Retro Command Line UI ───────────────────
def draw_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT)
    print("╔══════════════════════════════╗")
    print("║     ★ MASTER·MIND  8-BIT ★    ║")
    print("╚══════════════════════════════╝" + Style.RESET_ALL)

def play():
    draw_banner()
    level = input("Choose difficulty (easy, medium, hard): ").strip().lower()
    config = DIFFICULTY_LEVELS.get(level, DIFFICULTY_LEVELS['medium'])
    game = Mastermind(**config)

    print(f"\nAvailable colors:")
    for c in config['colors']:
        print(f"  {COLOR_MAP.get(c, '')}{c} = {BLOCK} {Style.RESET_ALL}")

    print(f"\nGuess the {game.code_length}-color code in {game.max_attempts} attempts!\n")

    while not game.is_over():
        try:
            guess = input(f"Attempt {game.attempts + 1}: ").strip().upper()
            result = game.guess(guess)

            print("Guess:   ", ' '.join(color_block(c) for c in guess))
            exact = f"{Fore.WHITE}●" * result['exact']
            partial = f"{Fore.LIGHTBLACK_EX}○" * result['partial']
            none = f"{Fore.BLACK}–" * (game.code_length - result['exact'] - result['partial'])

            print("Feedback:", exact + partial + none + Style.RESET_ALL)
            print(f"{Style.DIM}(● = exact, ○ = partial, – = miss)\n")

        except ValueError as ve:
            print(Fore.YELLOW + str(ve))

    print(Fore.GREEN + ("\n🎉 You cracked the code!" if game.is_won()
          else f"\n💥 Game over! The code was: {' '.join(color_block(c) for c in game.reveal_code())}"))


# ─── API Exposure ────────────────────────────
def create_game(difficulty="medium", secret_code=None):
    config = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS["medium"])
    game = Mastermind(**config)
    if secret_code:
        game.secret_code = list(secret_code.upper())
    return game

# ─── Run CLI ─────────────────────────────────
if __name__ == "__main__":
    play()