"""Main menu for the interactive 8-puzzle terminal application."""
from puzzle.puzzles import EASY_START, GOAL_STATE, HARD_START, MEDIUM_START, random_puzzle
from puzzle.state import Puzzle
from puzzle.tui import clear_console, interactive_play, playback_solution

PRESETS = {
    "1": ("Easy", EASY_START),
    "2": ("Medium", MEDIUM_START),
    "3": ("Hard", HARD_START),
}


def _select_start() -> Puzzle | None:
    print("Choose a starting puzzle:")
    for key, (label, _) in PRESETS.items():
        print(f"{key}. {label}")
    print("4. Randomize a starting puzzle")

    choice = input("Enter your choice: ").strip()
    if choice in PRESETS:
        return PRESETS[choice][1]
    if choice == "4":
        return random_puzzle()

    print("Invalid option.")
    return None


def main() -> None:
    while True:
        clear_console()
        print("8-Puzzle")
        print("")
        print("1. Watch A* solve a puzzle")
        print("2. Play a puzzle manually")
        print("0. Exit")
        print("")
        option = input("Enter your choice: ").strip()

        if option == "0":
            print("Goodbye.")
            return
        if option not in ("1", "2"):
            print("Invalid option.")
            continue

        start = _select_start()
        if start is None:
            input("Press Enter to continue...")
            continue

        if option == "1":
            playback_solution(start, GOAL_STATE)
        else:
            interactive_play(start, GOAL_STATE)

        input("Press Enter to return to the main menu...")


if __name__ == "__main__":
    main()
