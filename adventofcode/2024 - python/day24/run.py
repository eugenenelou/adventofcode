import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cache
from operator import itemgetter
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_start_values, raw_operations = content.split("\n\n")
    start_values = {}
    for line in raw_start_values.split("\n"):
        key, value = line.split(": ")
        start_values[key] = bool(int(value))

    operations = {}
    for line in raw_operations.split("\n"):
        raw, result = line.split(" -> ")
        operations[result] = raw.split(" ")
    return start_values, operations


def get_int(prefix: str, keys, get_value):
    znames = sorted((key for key in keys if key.startswith(prefix)), reverse=True)
    # print('znames', znames)
    zvalues = [str(int(get_value(name))) for name in znames]
    # print('zvalues', zvalues)
    return int("".join(zvalues), 2)


def main1(input_):
    start_values, operations = input_

    @cache
    def get_value(name):
        if (value := start_values.get(name)) is not None:
            return value
        a, op, b = operations[name]

        va = get_value(a)
        vb = get_value(b)
        match op:
            case "AND":
                return va and vb
            case "OR":
                return va or vb
            case "XOR":
                return va ^ vb

    return get_int("z", operations, get_value)


N_PAIRS = 4


sys.setrecursionlimit(100)


def main2(input_):
    start_values, operations = input_
    start_values = start_values.copy()

    reversed_operations = {}
    for k, v in operations.items():
        a, b, c = v
        reversed_operations[(a, b, c)] = k
        reversed_operations[(c, b, a)] = k

    to_swap = []
    for i in range(2, 45):
        a, op, b = operations[f"z{i:02d}"]
        if op != "XOR":
            print(f"z{i:02d} should be a XOR")
            to_swap.append(f"z{i:02d}")
            parent = reversed_operations[(f"x{i:02d}", "XOR", f"y{i:02d}")]
            key = next(
                k
                for k, (a, op, b) in operations.items()
                if op == "XOR" and (a == parent or b == parent)
            )
            print(f"should swap with {key=}")
            to_swap.append(key)
            continue

        try:
            a1, op1, b1 = operations[a]
            a2, op2, b2 = operations[b]
        except KeyError:
            continue

        if {op2, op1} != {"XOR", "OR"}:
            print(f"a op: {op1=}, b op:{op2=}; expected XOR and OR")
            if op1 == "OR":
                to_swap.append(b)
                parent = reversed_operations[(f"x{i:02d}", "XOR", f"y{i:02d}")]
                print(f"neet to swap {b=} with {parent=}")
                to_swap.append(parent)

            if op2 == "OR":
                to_swap.append(a)
                parent = reversed_operations[(f"x{i:02d}", "XOR", f"y{i:02d}")]
                print(f"neet to swap {a=} with {parent=}")
                to_swap.append(parent)

    assert len(set(to_swap)) == 8
    print("to_swap", to_swap)

    @cache
    def get_value(name):
        if (value := start_values.get(name)) is not None:
            return value
        a, op, b = operations[name]

        va = get_value(a)
        vb = get_value(b)
        match op:
            case "AND":
                return va and vb
            case "OR":
                return va or vb
            case "XOR":
                return va ^ vb

    def swap(eight_keys, operations):
        for i in range(0, len(eight_keys), 2):
            a, b = eight_keys[i], eight_keys[i + 1]
            operations[a], operations[b] = operations[b], operations[a]

    swap(to_swap, operations)

    x = get_int("x", start_values, lambda x: start_values[x])
    y = get_int("y", start_values, lambda y: start_values[y])
    z = get_int("z", operations, get_value)

    print("x", x)
    print("y", y)
    print("x+y", x + y)
    print(f"{x+y:045b}")
    print(f"{z:045b}")
    print("z", z)

    assert x + y == z

    return ",".join(sorted(to_swap))


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
