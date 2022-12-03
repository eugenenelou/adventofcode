import sys
from pathlib import Path
import string

values = {letter: i + 1 for i, letter in enumerate(string.ascii_letters)}


def parse_input(path: str, second=False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        l = len(line)
        if second:
            yield line
        else:
            yield line[: l // 2], line[l // 2 :]


def main1(input_):
    return sum(values[list(set(r1) & set(r2))[0]] for r1, r2 in input_)


def main2(input_):
    result = 0
    for i in range(0, len(input_), 3):
        b1, b2, b3 = input_[i : i + 3]
        result += values[list(set(b1) & set(b2) & set(b3))[0]]
    return result


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input = list(parse_input(input_filepath, second=second_part))
    if second_part:
        print(f"result: {main2(input)}", file=sys.stdout)
    else:
        print(f"result: {main1(input)}", file=sys.stdout)
