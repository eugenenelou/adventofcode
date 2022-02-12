import sys


def parse_input(input):
    pass


def main1(input):
    data = parse_input(input)


def main2(input):
    data = parse_input(input)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
