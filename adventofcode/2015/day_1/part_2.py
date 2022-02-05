import sys


def main(input):
    level = 0
    for i, c in enumerate(input):
        level += 1 if c == "(" else -1
        if level == -1:
            return i + 1


if __name__ == "__main__":
    input = next(iter(sys.stdin))
    print(main(input), file=sys.stdout)
