from pathlib import Path
from sys import argv

import solns

def get_input(day: int) -> str:
    with open(Path(__file__).parent.parent / "inputs" / f"input_{day}.txt") as input_file:
        input = input_file.read()
    return input

def run_day(day: int) -> None:
    {
        1: solns.day_1.run
    }.get(
        day,
        lambda _: print("No such day exists yet!")
        )(get_input(day))

def main():
    if len(argv) < 2:
        print("Please provide a day number as an argument.")
        return

    run_day(int(argv[1]))

if __name__ == "__main__":
    main()
