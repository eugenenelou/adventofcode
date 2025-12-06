from bisect import bisect_left
import sys
from pathlib import Path
from typing import Never
from utils.parser import MultiGroupsParser, IterableParser, FnParser, parse_int_pair

type Data = tuple[list[tuple[int, int]], list[int]]


parser = MultiGroupsParser[Data, list[Any]](
    [
        IterableParser[Data, list[Never]](FnParser(parse_int_pair)),
        IterableParser[Data, list[list[tuple[int, int]]]](FnParser(int)),
    ]
)

def standardize_ranges(ranges: list[tuple[int, int]]):
    ranges.sort()
    res = ranges[:1]
    for range_ in ranges[1:]:
        a_last, b_last = res[-1]
        a, b = range_
        if a <= b_last + 1:
            if b > b_last:
                res[-1] = (a_last, b)
        else:
            res.append(range_)

    for range1, range2 in zip(res[:-1], res[1:]):
        assert range1[0] <= range1[1] < range2[0] + 1 <= range2[1] + 1, (range1, range2)
    return res


def main1(data: Data):
    # print('data', data)
    fresh_ingredient_ranges, all_ingredient_ids = data
    ranges = standardize_ranges(fresh_ingredient_ranges)
    range_starts = [start for start, _ in ranges]
    range_len = len(ranges)

    res = 0
    for ingredient in all_ingredient_ids:
        idx = bisect_left(range_starts, ingredient)
        if idx < range_len:
            a, _ = ranges[idx]
            if ingredient == a:
                res += 1
                continue
        if idx > 0:
            _, prev_b = ranges[idx-1]
            if ingredient <= prev_b:
                res += 1
    return res


def main2(data: Data):
    fresh_ingredient_ranges, _ = data
    ranges = standardize_ranges(fresh_ingredient_ranges)
    return sum(b - a + 1 for a, b in ranges)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
