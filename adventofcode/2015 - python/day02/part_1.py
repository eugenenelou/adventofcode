import sys


def min_2(a, b, c):
    if a > b:
        return (b, min(a, c))
    return (a, min(b, c))


def main(input):
    sum = 0
    for line in input:
        a, b, c = map(int, line.split("x"))
        sum += 2 * (a * b + b * c + a * c)
        x, y = min_2(a, b, c)
        sum += x * y
    return sum


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
