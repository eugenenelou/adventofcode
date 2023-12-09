import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [[int(x) for x in row.split()] for row in content.split("\n")]


def solve(numbers: list[int]) -> int:
    if not any(numbers):
        return 0
    return numbers[-1] + solve([b - a for a, b in zip(numbers[:-1], numbers[1:])])


def main1(input_):
    return sum(solve(numbers) for numbers in input_)


def solve2(numbers: list[int]) -> int:
    if not any(numbers):
        return 0
    return numbers[0] - solve2([b - a for a, b in zip(numbers[:-1], numbers[1:])])


def main2(input_):
    return sum(solve2(numbers) for numbers in input_)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
