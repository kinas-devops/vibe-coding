# Mastermind AI Experiments 🧠🎮

This repository showcases a collection of Mastermind solvers ranging from classic logic-based strategies (like Knuth and constraint propagation) to deep reinforcement learning agents. The goal is to explore, compare, and learn from a variety of algorithmic approaches to this classic puzzle game.

About MasterMind game:
https://en.wikipedia.org/wiki/Mastermind_(board_game)

Each solver was built collaboratively with the help of Microsoft AI Copilot to blend clear logic, clean code structure, and insightful experimentation.

First, we needed a nice visual to manage the MasterMind game.
After some tries and adjusts it was created to be the most versatile and adaptable, with the help of Microsoft AI Copilot.
The last functional version was called "retro_mastermind.py" and uses colors and emoticons to the console, to be more friendly to user.

Some time ago I created a standalone python code based on the Knuth solver approach, so this was the first solver to be implemented in vibe-coding.
https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm

For an easy use, I ask AI Copilot to generate 2 code files: 1 code file has the solver (<algorithm>_solver.py), 1 code file as the driver to play (<algorithm>_vs_retro.py)
Because AI algorithms need to be trained, these versions have additional file for training (<algorithm>_train.py)
The AI train creates files with the trained model for each difficulty level, which can be used later in the solver code.



> 💡 Dive into logic trees, entropy explorers, hybrid DRL brains, and more.