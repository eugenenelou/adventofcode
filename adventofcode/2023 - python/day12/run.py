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


def split_row_in_masks(row: str) -> tuple:
    return tuple(filter(bool, re.split(r"\.+", row)))


@cache
def count_row(
    masks: tuple, group_sizes: tuple[int], mask_total: int, group_total: int
) -> int:
    if mask_total < group_total:
        return 0
    if len(group_sizes) == 0:
        # print("a")
        return 1 if all(char == "?" for mask in masks for char in mask) else 0
    if len(masks) == 0:
        # print("a'")
        return 0
    mask = masks[0]
    if not mask:
        return count_row(masks[1:], group_sizes, mask_total - len(mask), group_total)
    group_size = group_sizes[0]

    if len(mask) < group_size:
        return (
            count_row(masks[1:], group_sizes, mask_total - len(mask), group_total)
            if all(char == "?" for char in mask)
            else 0
        )
    if len(mask) == group_size:
        # print("b", mask)
        return count_row(
            masks[1:], group_sizes[1:], mask_total - len(mask), group_total - group_size
        ) + (
            count_row(masks[1:], group_sizes, mask_total - len(mask), group_total)
            if all(char == "?" for char in mask)
            else 0
        )
    elif all(char == "#" for char in mask):
        # print("c")
        return 0
    if mask[group_size] == "?":
        # print("F")
        return (
            count_row(
                (mask[group_size + 1 :], *masks[1:]),
                group_sizes[1:],
                mask_total - len(mask[: group_size + 1]),
                group_total - group_size,
            )
        ) + (
            count_row(
                (mask[1:], *masks[1:]),
                group_sizes,
                mask_total - len(mask[:1]),
                group_total,
            )
            if mask[0] == "?"
            else 0
        )
    else:
        # print("G")
        return (
            count_row(
                (mask[1:], *masks[1:]),
                group_sizes,
                mask_total - len(mask[:1]),
                group_total,
            )
            if mask[0] == "?"
            else 0
        )


def main1(input_):
    res = 0
    for i, (row, group_sizes) in enumerate(input_):
        # print(i)
        masks = split_row_in_masks(row)
        count = count_row(
            masks,
            group_sizes,
            mask_total=sum(len(mask) for mask in masks),
            group_total=sum(group_sizes),
        )
        res += count
    return res


def main2(input_):
    input2 = [
        (
            "?".join(row for _ in range(5)),
            group_sizes * 5,
        )
        for row, group_sizes in input_
    ]
    # print("input2", input2)
    return main1(input2)


def main3(input_):
    """For the fun of it, concatenate every line"""
    sys.setrecursionlimit(100_000)
    input3 = [
        (
            "?".join(row for row, _ in input_),
            tuple(size for _, group_sizes in input_ for size in group_sizes),
        )
    ]
    # print("input3", input3)
    return main1(input3)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    third_part = len(sys.argv) > 2 and sys.argv[2] == "--three"
    input_ = parse_input(input_filepath)
    if third_part:
        print(f"result: {main3(input_)}", file=sys.stdout)
    elif second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
