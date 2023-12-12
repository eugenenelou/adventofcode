import re
import sys
from functools import cache
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        chars, group_sizes = row.split(" ")
        res.append((chars, tuple(map(int, group_sizes.split(",")))))
    return res


def split_row_in_masks(row: str) -> list[str]:
    return re.split(r"\.+", row)


# def count_group(group: str, list[int]) -> int:
#     pass


# assert count_group("???", (1, 1)) == 1
# assert count_group("????", (1, 1)) == 3
# assert count_group("?#??", (1, 1)) == 1


@cache
def count(mask: str, group_size: int):
    pass


def count_row(masks: list[str], group_sizes: tuple[int], acc: int = 0) -> int:
    if len(masks) == 0 or len(group_sizes) == 0:
        print("a")
        return 0
    mask = masks[0]
    group_size = group_sizes[0]
    if len(mask) == group_size:
        print("b", mask)
        return acc and acc * count_row(masks[1:], group_sizes[1:])
    elif all(char == "#" for char in mask):
        print("c")
        return 1

    if len(mask) < group_size:
        if any(char == "#" for char in mask):
            # it should fit because the # is mandatory
            print("d")
            return 0
        else:
            print("E")
            return acc and acc * count_row(masks[1:], group_sizes)
    if mask[group_size] in (".", "?"):
        print("F")
        return count_row(
            [mask[group_size + 1 :], *masks[1:]], group_sizes[1:], acc=acc + 1
        )
    else:
        print("G")
        return count_row([mask[1:], *masks[1:]], group_sizes, acc=acc)


def main1(input_):
    res = 0
    for row, group_sizes in input_:
        print("\nrow", row, group_sizes)
        count = count_row(split_row_in_masks(row), group_sizes)
        print("count", count)
        res += count
    return res


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
