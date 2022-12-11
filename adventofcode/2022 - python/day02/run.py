import sys
from pathlib import Path

values_1 = {
    "A X": 3 + 1,
    "A Y": 6 + 2,
    "A Z": 3,
    "B X": 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 6 + 1,
    "C Y": 2,
    "C Z": 3 + 3,
}

values_2 = {
    "A X": 3,
    "A Y": 3 + 1,
    "A Z": 6 + 2,
    "B X": 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 2,
    "C Y": 3 + 3,
    "C Z": 6 + 1,
}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def main(input_, values):
    return sum(values[line] for line in input_)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main(input_, values_2)}", file=sys.stdout)
    else:
        print(f"result: {main(input_, values_1)}", file=sys.stdout)
