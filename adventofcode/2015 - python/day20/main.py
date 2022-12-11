import sys

from functools import reduce


def factors(n):
    return set(
        reduce(list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0))
    )


def parse_input(input):
    return int(next(iter(input)).rstrip())


def count_gifts(i):
    return 10 * sum(factors(i))


def count_gifts2(i):
    return 11 * sum(f if i // f <= 50 else 0 for f in factors(i))


def main1(input):
    n = parse_input(input)
    return next(i for i in range(1, n // 10) if count_gifts(i) >= n)


def main2(input):
    n = parse_input(input)
    return next(i for i in range(1, n // 10) if count_gifts2(i) >= n)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
