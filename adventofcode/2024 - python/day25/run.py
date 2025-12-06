import sys
from pathlib import Path


def parse_pattern(lines):
    res = [-1] * 5
    for line in lines:
        for i, char in enumerate(line):
            if char == "#":
                res[i] += 1
    return res


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    patterns = content.split("\n\n")
    keys = []
    locks = []
    for pattern in patterns:
        lines = pattern.split("\n")
        dimensions = parse_pattern(lines)
        (locks if pattern[0] == "." else keys).append(dimensions)

    return locks, keys


def main1(input_):
    locks, keys = input_
    return sum(
        1
        for lock in locks
        for key in keys
        if all(a + b < 6 for a, b in zip(lock, key, strict=True))
    )


def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
