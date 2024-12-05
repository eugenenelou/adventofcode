import sys
from functools import cmp_to_key, partial
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_rules, raw_manuals = content.split("\n\n")
    rules = [
        (int(a), int(b))
        for a, b in map(partial(str.split, sep="|"), raw_rules.split("\n"))
    ]
    manuals = [list(map(int, manual.split(","))) for manual in raw_manuals.split("\n")]
    return rules, manuals


def is_ok(rules: list[tuple[int, int]], manual: list[int]):
    pages = len(manual)
    for i in range(pages - 1):
        for j in range(i + 1, pages):
            if (manual[i], manual[j]) not in rules:
                return False
    return True


def main1(input_):
    rules, manuals = input_
    res = 0
    for manual in manuals:
        if is_ok(rules, manual):
            res += manual[len(manual) // 2]

    return res


def correct_manual(rules: list[tuple[int, int]], manual: list[int]):
    def compare(x, y):
        if (x, y) in rules:
            return -1
        return 1

    return sorted(manual, key=cmp_to_key(compare))


def main2(input_):
    rules, manuals = input_
    res = 0
    for manual in manuals:
        if not is_ok(rules, manual):
            manual = correct_manual(rules, manual)
            res += manual[len(manual) // 2]

    return res


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
