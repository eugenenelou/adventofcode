import sys


def main(input):
    result = 0
    for string in input:
        result += 2  # the start and end quotes
        for c in string:
            if c == '"' or c == "\\":
                result += 1
    return result


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
