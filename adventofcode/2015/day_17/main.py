from itertools import combinations
import sys

TOTAL = 150


def parse_input(input):
    return [int(v.rstrip()) for v in input]


def main1(input):
    data = parse_input(input)
    return sum(
        1
        for r in range(len(data))
        for combination in combinations(data, r + 1)
        if sum(combination) == TOTAL
    )


def main2(input):
    data = parse_input(input)
    for r in range(len(data)):
        s = sum(1 for combination in combinations(data, r + 1) if sum(combination) == TOTAL)
        if s > 0:
            return s


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
