import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    coords = []
    for raw in content.split("\n"):
        a, b = raw.split(",")
        coords.append((int(a), int(b)))
    H = max(a for a, _ in coords) + 1
    W = max(b for _, b in coords) + 1
    return H, W, coords


def construct_grid(H, W, coords):
    grid = [[False] * W for _ in range(H)]
    for i, (x, y) in enumerate(coords):
        grid[x][y] = True
    return grid


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def display_grid(grid):
    for row in grid:
        print("".join(("#" if block else "." for block in row)))


def main1(input_):
    H, W, coords = input_
    grid = construct_grid(H, W, coords[:1024])

    display_grid(grid)

    paths_reached = {(0, 0)}
    paths = [(0, 0)]
    i = 0
    while paths:
        new_paths = []
        for x, y in paths:
            for dx, dy in DIRECTIONS:
                new_x = x + dx
                new_y = y + dy
                if (
                    (new_x, new_y) in paths_reached
                    or new_x < 0
                    or new_x >= H
                    or new_y < 0
                    or new_y >= W
                ):
                    continue

                if new_x == H - 1 and new_y == W - 1:
                    return i + 1
                if not grid[new_x][new_y]:
                    paths_reached.add((new_x, new_y))
                    new_paths.append((new_x, new_y))
        paths = new_paths
        i += 1


def has_solution(H, W, coords, cutoff):
    grid = construct_grid(H, W, coords[:cutoff])

    paths_reached = {(0, 0)}
    paths = [(0, 0)]
    i = 0
    found = False
    while paths and not found:
        new_paths = []
        for x, y in paths:
            for dx, dy in DIRECTIONS:
                new_x = x + dx
                new_y = y + dy
                if (
                    (new_x, new_y) in paths_reached
                    or new_x < 0
                    or new_x >= H
                    or new_y < 0
                    or new_y >= W
                ):
                    continue

                if new_x == H - 1 and new_y == W - 1:
                    found = True
                if not grid[new_x][new_y]:
                    paths_reached.add((new_x, new_y))
                    new_paths.append((new_x, new_y))
        paths = new_paths
        i += 1
    return found


def main2(input_):
    H, W, coords = input_

    # binary search
    solution = 1024
    impossible = len(coords)
    while solution + 1 < impossible:
        test = (solution + impossible) // 2
        if has_solution(H, W, coords, test):
            solution = test
        else:
            impossible = test
    return coords[solution]


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
