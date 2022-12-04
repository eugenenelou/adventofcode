import sys

import re

input_regex = re.compile(r"(\d+)[^\d]+(\d+)")


def get_nth_code(n):
    res = 20151125
    if n == 1:
        return res
    for _ in range(1, n):
        res = (res * 252533) % 33554393
    return res


def get_n_from_coord(x, y):
    n = x + y - 2  # last complete diagonal
    return n * (n + 1) // 2 + y


def parse_input(input_):
    match = input_regex.search(input_)
    return int(match.group(1)), int(match.group(2))


def run(x, y):
    return get_nth_code(get_n_from_coord(x, y))


if __name__ == "__main__":
    input_ = next(iter(sys.stdin))
    second_part = "--two" in sys.argv

    print("inp", input_)

    print(run(*parse_input(input_)), file=sys.stdout)
