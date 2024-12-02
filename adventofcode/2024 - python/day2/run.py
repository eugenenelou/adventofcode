import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [list(map(int, line.split())) for line in content.split("\n")]


def is_safe(line: list[int], retry=False):
    a = line[0]
    b = line[-1]
    if a > b:
        inc = False
    elif a < b:
        inc = True
    else:
        return False
    for a, b in zip(line[:-1], line[1:]):
        try:
            assert a != b, "toto"
            assert (a < b) is inc, "b"
            assert 1 <= abs(a - b) <= 3, "c"
        except AssertionError:
            return False
    return True


def is_safe2(line: list[int], retry=False):
    a = line[0]
    b = line[-1]
    if a > b:
        inc = False
    elif a < b:
        inc = True
    else:
        return False
    for i, (a, b) in enumerate(zip(line[:-1], line[1:])):
        try:
            assert a != b, "toto"
            assert (a < b) is inc, "b"
            assert 1 <= abs(a - b) <= 3, "c"
        except AssertionError:
            if retry:
                return False
            else:
                return is_safe2(line[:i] + line[i + 1 :], True) or is_safe2(
                    line[: i + 1] + line[i + 2 :], True
                )
    return True


def main1(input_):
    return sum(is_safe(line) for line in input_)


def main2(input_):
    return sum(is_safe2(line) for line in input_)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
