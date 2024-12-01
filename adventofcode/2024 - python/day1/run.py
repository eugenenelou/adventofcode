import sys
from collections import Counter
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    left, right = [], []
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        a, b = line.split("   ")
        left.append(int(a))
        right.append(int(b))
    return left, right


def main1(input_):
    left, right = input_
    left.sort()
    right.sort()
    return sum(abs(a - b) for a, b in zip(left, right, strict=True))


def main2(input_):
    left, right = input_
    right_counter = Counter(right)
    return sum(a * right_counter[a] for a in left)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
