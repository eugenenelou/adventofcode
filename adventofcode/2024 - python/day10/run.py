import operator
import sys
from collections import defaultdict
from functools import reduce
from itertools import chain
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [list(map(int, line)) for line in content.split("\n")]


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def compute_valid_directions(grid):
    W = len(grid[0])
    H = len(grid)
    valid_directions = [[[] for _ in range(W)] for _ in range(H)]
    for x, line in enumerate(grid):
        for y, cell in enumerate(line):
            if cell == 9:
                continue
            value = line[y]
            for dx, dy in DIRECTIONS:
                if (
                    0 <= x + dx < W
                    and 0 <= y + dy < H
                    and grid[x + dx][y + dy] == value + 1
                ):
                    valid_directions[x][y].append((dx, dy))

    return valid_directions


def find_solution(input_, deduplicate: bool):
    res = 0
    valid_directions = compute_valid_directions(input_)

    def find_paths(x, y, acc=9) -> int:
        if acc == 0:
            return [(x, y)]
        return chain(
            *(find_paths(x + dx, y + dy, acc - 1) for dx, dy in valid_directions[x][y])
        )

    for row, line in enumerate(input_):
        for col, cell in enumerate(line):
            if cell == 0:
                paths = find_paths(row, col)
                res += len(set(paths) if deduplicate else list(paths))
    return res


def main1(input_):
    return find_solution(input_, deduplicate=True)


def main2(input_):
    return find_solution(input_, deduplicate=False)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
