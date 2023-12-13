import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [pattern.split("\n") for pattern in content.split("\n\n")]


def is_symmetrical(s: str, idx: int) -> bool:
    for i in range(min(idx, len(s) - idx)):
        if s[idx + i] != s[idx - i - 1]:
            return False
    return True


def find_pattern(pattern: list[str]) -> tuple[int, int]:
    for i in range(1, len(pattern[0])):
        if all(is_symmetrical(row, i) for row in pattern):
            return 0, i
    t_pattern = [
        [pattern[i][j] for i in range(len(pattern))] for j in range(len(pattern[0]))
    ]
    for i in range(1, len(pattern)):
        if all(is_symmetrical(row, i) for row in t_pattern):
            return i, 0
    for row in pattern:
        print(row)
    raise Exception("mirror not found")


def main1(input_):
    horizontal = 0
    vertical = 0
    for pattern in input_:
        h, v = find_pattern(pattern)
        horizontal += h
        vertical += v
    return vertical + 100 * horizontal


def count_symmetrical_diffs(s: str, idx: int) -> int:
    return sum(
        (1 if s[idx + i] != s[idx - i - 1] else 0)
        for i in range(min(idx, len(s) - idx))
    )


def find_pattern2(pattern: list[str]) -> tuple[int, int]:
    for i in range(1, len(pattern[0])):
        if sum(count_symmetrical_diffs(row, i) for row in pattern) == 1:
            return 0, i
    t_pattern = [
        [pattern[i][j] for i in range(len(pattern))] for j in range(len(pattern[0]))
    ]
    for i in range(1, len(pattern)):
        if sum(count_symmetrical_diffs(row, i) for row in t_pattern) == 1:
            return i, 0
    for row in pattern:
        print(row)
    raise Exception("mirror not found")


def main2(input_):
    horizontal = 0
    vertical = 0
    for pattern in input_:
        h, v = find_pattern2(pattern)
        horizontal += h
        vertical += v
    return vertical + 100 * horizontal


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
