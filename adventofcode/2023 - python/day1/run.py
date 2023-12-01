import sys
from pathlib import Path
import re


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def get_first_digit(row: str):
    return next(int(c) for c in row if c.isdigit())


def main1(input_):
    """Get the first digit of each row and reversed row"""
    return sum(get_first_digit(row) * 10 + get_first_digit(row[::-1]) for row in input_)


digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_pattern = re.compile(rf"(\d|{'|'.join(digits)})")
reverse_digit_pattern = re.compile(rf"(\d|{'|'.join(word[::-1] for word in digits)})")

values = {
    **{str(i): i for i in range(10)},
    **{word: i for i, word in enumerate(digits)},
}


def main2(input_):
    """Get the first digit or digit word of each row and reversed row by regex search"""
    s = 0
    for row in input_:
        s += (
            values[digit_pattern.search(row).group(0)] * 10
            + values[reverse_digit_pattern.search(row[::-1]).group(0)[::-1]]
        )
    return s


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
