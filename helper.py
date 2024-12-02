#!/usr/bin/env python

import os
import subprocess

from argparse import ArgumentParser, Namespace
from json import dumps, loads
from pathlib import Path
from shlex import split
from sys import argv, version_info
from venv import create

assert version_info.minor >= 10, "Python 3.10 or higher is required."

AOC_ROOT = Path(__file__).parent
os.chdir(AOC_ROOT)


def init_check() -> None:
    venv_path = AOC_ROOT / "python/.venv"
    input_dir = AOC_ROOT / "inputs"

    if not venv_path.exists():
        create(venv_path, with_pip=True)
        print(f"Virtual environment created at {venv_path}.")

    assert (
        subprocess.run(
            split(
                f'{venv_path}/bin/pip install -r {Path(__file__).parent / "requirements.txt"}'
            )
        ).returncode
        == 0
    ), "Failed to install requirements"

    if not input_dir.exists():
        input_dir.mkdir()
        (AOC_ROOT / "python/inputs").symlink_to(input_dir)
        (AOC_ROOT / "rust/inputs").symlink_to(input_dir)
        print(
            f"Input directory created at {input_dir} and symlinked to python and rust directories."
        )

    if not (AOC_ROOT / ".env").exists():
        with open(AOC_ROOT / ".env", "w") as f:
            f.write(
                dumps({"AOC_SESSION_COOKIE": input("Enter your AoC session cookie: ")})
            )
        print(f"Created .env file at {AOC_ROOT}.")

    os.environ["AOC_SESSION_COOKIE"] = loads((AOC_ROOT / ".env").read_text()).get(
        "AOC_SESSION_COOKIE", ""
    )
    assert (
        os.environ["AOC_SESSION_COOKIE"] != ""
    ), "AoC session cookie not found in .env file."

    print("Initialization complete.")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-i", "--get-input", type=int)
    parser.add_argument("-r", "--run", type=int)

    return parser.parse_args(argv)


def download_input(day: int) -> None:
    import requests

    url = f"https://adventofcode.com/2024/day/{day}/input"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0, i",
        "TE": "trailers",
    }

    response = requests.get(
        url, headers=headers, cookies={"session": os.environ["AOC_SESSION_COOKIE"]}
    )
    assert response.status_code == 200, "GET request failed"
    with open(AOC_ROOT / f"inputs/input_{day}.txt", "w") as input_fl:
        input_fl.write(response.text)


def run(day: int):
    if not (AOC_ROOT / f"inputs/input_{day}.txt").exists():
        download_input(day)

    print("Rust:")
    os.chdir(AOC_ROOT / "rust")
    subprocess.run(split(f"cargo run --release -- {day}"))

    print()

    print("Python:")
    os.chdir(AOC_ROOT / "python")
    subprocess.run(
        split(
            f"{AOC_ROOT / 'python/.venv/bin/python'} {AOC_ROOT / 'python/src/main.py'} {day}"
        )
    )

    os.chdir(AOC_ROOT)


def main():
    try:
        args = parse_args()
        if args.get_input:
            download_input(args.get_input)
        if args.run:
            run(args.run)
    finally:
        os.environ["AOC_SESSION_COOKIE"] = ""


if __name__ == "__main__":
    main()
