import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        target, values = row.split(": ")
        res.append((int(target), list(map(int, values.split()))))
    return res


def is_achievable(target: int, values: list[int], acc: int) -> bool:
    if len(values) == 0:
        return acc == target
    first_value, *rest = values
    return is_achievable(target, rest, acc + first_value) or is_achievable(
        target, rest, acc * first_value
    )


def main1(input_):
    return sum(
        target
        for target, values in input_
        if is_achievable(target, values[1:], values[0])
    )


def is_achievable2(target: int, values: list[int], acc: int) -> bool:
    if len(values) == 0:
        return acc == target
    elif values[0] > target:
        return False
    first_value, *rest = values
    return (
        is_achievable2(target, rest, acc + first_value)
        or is_achievable2(target, rest, acc * first_value)
        or is_achievable2(target, rest, int(str(acc) + str(first_value)))
    )


def main2(input_):
    return sum(
        target
        for target, values in input_
        if is_achievable2(target, values[1:], values[0])
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
