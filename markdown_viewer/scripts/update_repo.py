#!/usr/bin/env python3
"""
Automates updating the Git repository by adding, committing, and pushing changes.

This script is a convenience wrapper around the common Git workflow:
1. `git add .`
2. `git commit -m \"<message>\"`
3. `git push origin main`

Usage:
    python scripts/update_repo.py \"Your commit message here\"
"""

import sys
import subprocess
import argparse

def run_command(command: list[str]):
    """Executes a shell command and exits if it fails."""
    print(f"\n--- Running command: {' '.join(command)} ---")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Is Git installed and in your PATH?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(e.stderr)
        sys.exit(1)

def main():
    """Main function to parse arguments and run Git commands."""
    parser = argparse.ArgumentParser(
        description="Automate adding, committing, and pushing changes to a Git repository."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The commit message."
    )
    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="The branch to push to (defaults to 'main')."
    )
    args = parser.parse_args()

    # --- Git Commands ---
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", args.message])
    run_command(["git", "push", "origin", args.branch])

    print("\n--- Successfully updated the repository! ---")

if __name__ == "__main__":
    main()
