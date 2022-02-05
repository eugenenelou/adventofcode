import sys


def main(input):
    return input.count("(") - input.count(")")


if __name__ == "__main__":
    input = next(iter(sys.stdin))
    print(main(input), file=sys.stdout)
