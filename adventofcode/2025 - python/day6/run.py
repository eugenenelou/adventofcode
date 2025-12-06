from functools import reduce
import operator
import re
import sys
from pathlib import Path
from typing import Literal
from utils.parser import IterableParser, FnParser

type Data = list[tuple[list[int], Literal["*", "+"]]]


def parse(lines):
    numbers = [[] for _ in range(len(lines[0]))]
    for i, line in enumerate(lines[:-1]):
        for j, number in enumerate(line):
            numbers[j].append(int(number))
    return list(zip(numbers, lines[-1], strict=True))


parser = IterableParser[Data, None](
    IterableParser[Data, None](
        FnParser(lambda x: x), separator=re.compile(r" "), filter=bool
    )
)


def apply(numbers: list[int], op: Literal["*", "+"]):
    return reduce(operator.add if op == "+" else operator.mul, numbers)


def main1(data: list[Data]):
    parsed_data = parse(data)
    return sum(apply(numbers, op) for numbers, op in parsed_data)


parser2 = IterableParser[list[str], None](FnParser(lambda x: x))


def parse2(data):
    idxs_to_split = set()
    numbers_count_by_operation = []
    count = 0
    for i, char in enumerate(data[-1]):
        if i > 0 and char != " ":
            idxs_to_split.add(i - 1)
            numbers_count_by_operation.append(count)
            count = 0
        elif i > 0:
            count += 1
    numbers_count_by_operation.append(count + 1)

    ops = [char for char in data[-1] if char != " "]

    numbers = [[[] for _ in range(count)] for count in numbers_count_by_operation]

    for i, line in enumerate(data[:-1]):
        number_offset = 0
        operations_idx = 0
        for j, c in enumerate(line):
            if c != " ":
                numbers[operations_idx][number_offset].append(c)
            if j in idxs_to_split:
                number_offset = 0
                operations_idx += 1
            else:
                number_offset += 1
    numbers = [
        [int("".join(raw_number)) for raw_number in raw_numbers]
        for raw_numbers in numbers
    ]
    return list(zip(numbers, ops, strict=True))


def main2(data: list[Data]):
    parsed_data = parse2(data)
    return sum(apply(numbers, op) for numbers, op in parsed_data)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    if second_part:
        input_ = parser2.parse(Path(input_filepath).read_text())
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        input_ = parser.parse(Path(input_filepath).read_text())
        print(f"result: {main1(input_)}", file=sys.stdout)
