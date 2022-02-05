import sys
import re


def main(input):
    grid = [[0] * 1000 for _ in range(1000)]
    for instruction in input:
        match re.split("[ ,]", instruction):
            case ["toggle", x1, y1, "through", x2, y2]:
                for row in grid[int(x1) : int(x2) + 1]:
                    for i in range(int(y1), int(y2) + 1):
                        row[i] += 2
            case ["turn", value, x1, y1, "through", x2, y2]:
                for row in grid[int(x1) : int(x2) + 1]:
                    for i in range(int(y1), int(y2) + 1):
                        row[i] = max(0, row[i] + (1 if value == "on" else -1))
    return sum(sum(row) for row in grid)


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
