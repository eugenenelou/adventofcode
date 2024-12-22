import sys
from functools import cache
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


coords_for_digits = {
    "A": (0, 2),
    "0": (0, 1),
    "1": (1, 0),
    "2": (1, 1),
    "3": (1, 2),
    "4": (2, 0),
    "5": (2, 1),
    "6": (2, 2),
    "7": (3, 0),
    "8": (3, 1),
    "9": (3, 2),
}

coords_for_arrows = {
    "A": (1, 2),
    "^": (1, 1),
    "<": (0, 0),
    "v": (0, 1),
    ">": (0, 2),
}


def compute_possibilities(list_of_parts: list[list[str]]) -> set[str]:
    res = {""}
    for parts in list_of_parts:
        new_res: set[str] = set()
        for part in parts:
            for prefix in res:
                new_res.add(f"{prefix}{part}A")
        res = new_res
    return res


@cache
def convert(value: str, for_digits: bool, current_pos="A") -> set[str]:
    coords = coords_for_digits if for_digits else coords_for_arrows

    def apply_y(y_diff, res):
        if y_diff > 0:
            res.extend(">" * y_diff)
        elif y_diff < 0:
            res.extend("<" * (-y_diff))

    def apply_x(x_diff, res):
        if x_diff > 0:
            res.extend("^" * x_diff)
        elif x_diff < 0:
            res.extend("v" * (-x_diff))

    list_of_parts: list[list[str]] = []

    for char in value:
        x_pos, y_pos = coords[current_pos]
        x_char, y_char = coords[char]

        y_diff = y_char - y_pos
        x_diff = x_char - x_pos

        parts = []
        # y first
        if (x_pos != 0 or y_char != 0) if for_digits else (x_pos != 1 or y_char != 0):
            part = []
            apply_y(y_diff, part)
            apply_x(x_diff, part)
            parts.append("".join(part))

        # x first
        if (y_pos != 0 or x_char != 0) if for_digits else (x_char != 1 or y_pos != 0):
            part = []
            apply_x(x_diff, part)
            apply_y(y_diff, part)
            parts.append("".join(part))

        list_of_parts.append(parts)
        current_pos = char
    return compute_possibilities(list_of_parts)


@cache
def get_recursive_arrows_min_length(part: str, depth: int, for_digits=False):
    if not part:
        return 0
    if depth == 0:
        return len(part)

    return min(
        sum(
            get_recursive_arrows_min_length(f"{sub_part}A", depth - 1)
            for sub_part in possibility[:-1].split("A")
        )
        for possibility in convert(part, for_digits)
    )


def main1(input_, n=2):
    res = 0
    for row in input_:
        min_len = get_recursive_arrows_min_length(row, depth=n + 1, for_digits=True)

        complexity = min_len * int(row[:-1])
        res += complexity
    return res


def main2(input_):
    return main1(input_, n=25)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
