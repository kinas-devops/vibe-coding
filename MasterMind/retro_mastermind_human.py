import random
import time
import os
import sys
from colorama import Fore, Style, init
init(autoreset=True)

# ╔═[ CONFIGURATION ]═╗
DIFFICULTY_LEVELS = {
    'easy': {'code_length': 3, 'colors': 'RGB', 'max_attempts': 12},
    'medium': {'code_length': 4, 'colors': 'RGBYOP', 'max_attempts': 10},
    'hard': {'code_length': 5, 'colors': 'RGBYOPCM', 'max_attempts': 8}
}

BLOCK = '█'
COLOR_MAP = {
    'R': Fore.RED,
    'G': Fore.GREEN,
    'B': Fore.BLUE,
    'Y': Fore.YELLOW,
    'O': Fore.MAGENTA,
    'P': Fore.CYAN,
    'C': Fore.LIGHTBLUE_EX,
    'M': Fore.LIGHTMAGENTA_EX
}

def color_block(char):
    return COLOR_MAP.get(char.upper(), Fore.WHITE) + BLOCK + Style.RESET_ALL

# ╔═[ GAME LOGIC ]═╗
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

# ╔═[ UI + ANIMATION ]═╗
def draw_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT)
    print("╔══════════════════════════════╗")
    print("║     ★ MASTER·MIND  8-BIT ★   ║")
    print("╚══════════════════════════════╝" + Style.RESET_ALL)

def animate_guess(pegs):
    for block in pegs:
        print('   ' + block, end='\r')
        time.sleep(0.1)
    print('   ' + ' '.join(pegs))

def play():
    draw_banner()
    level = input("Choose difficulty (easy, medium, hard): ").strip().lower()
    config = DIFFICULTY_LEVELS.get(level, DIFFICULTY_LEVELS['medium'])

    game = Mastermind(**config)

    #print(f"\nAvailable colors: ", end="")
    #for c in config['colors']:
    #    print(color_block(c), end=" ")
    
    print(f"\nAvailable colors:")
    for c in config['colors']:
        print(f"  {COLOR_MAP.get(c, '')}{c} = {BLOCK} {Style.RESET_ALL}")

    print(f"\n\nGuess the {game.code_length}-color code in {game.max_attempts} attempts!\n")

    while not game.is_over():
        try:
            guess = input(f"Attempt {game.attempts + 1}: ").strip().upper()
            result = game.guess(guess)
            colored = [color_block(c) for c in guess]
            animate_guess(colored)

            # print(f"{Fore.WHITE}Feedback: {Fore.WHITE}●" * result['exact'] +
            #      f"{Fore.LIGHTBLACK_EX}○" * result['partial'] + "\n")
            print("Feedback:", end=" ")

            exact = f"{Fore.WHITE}●" * result['exact']
            partial = f"{Fore.LIGHTBLACK_EX}○" * result['partial']
            none = f"{Fore.BLACK}–" * (game.code_length - result['exact'] - result['partial'])

            print(exact + partial + none + Style.RESET_ALL)
            print(f"{Style.DIM}(● = exact match, ○ = partial match, – = miss)\n")

        except ValueError as ve:
            print(Fore.YELLOW + str(ve))

    if game.is_won():
        print(Fore.GREEN + Style.BRIGHT + "\n🎉 You cracked the code! You're a Mastermind!")
    else:
        print(Fore.RED + "\n💥 Game over! The correct code was: ", end="")
        print(' '.join(color_block(c) for c in game.reveal_code()))


def create_game(difficulty="medium"):
    config = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS["medium"])
    return Mastermind(**config)

# ╔═[ LAUNCH ]═╗
if __name__ == "__main__":
    play()