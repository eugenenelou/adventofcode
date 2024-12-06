from copy import deepcopy
from itertools import cycle
import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    grid = content.split("\n")
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            if char == "^":
                grid[x] = grid[x].replace("^", ".")
                return [list(line) for line in grid], (x, y)


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class LoopException(Exception):
    pass


def find_original_path(grid, start_location):
    direction_cycle = cycle(DIRECTIONS)
    dx, dy = next(direction_cycle)
    (x, y) = start_location
    H = len(grid)
    W = len(grid[0])
    seen_locations = {(x, y)}
    seen_locations_with_direction = {(x, y, dx, dy)}
    new_x = x + dx
    new_y = y + dy
    while new_x < H and new_y < W and new_x >= 0 and new_y >= 0:
        if grid[new_x][new_y] == "#":
            dx, dy = next(direction_cycle)
        else:
            x = new_x
            y = new_y
            seen_locations.add((x, y))
            if (x, y, dx, dy) in seen_locations_with_direction:
                raise LoopException("found a loop")
            seen_locations_with_direction.add((x, y, dx, dy))
        new_x = x + dx
        new_y = y + dy
    return seen_locations


def main1(input_):
    grid, start_location = input_
    seen_locations = find_original_path(grid, start_location)
    return len(seen_locations)


def is_loop_with_obstacle(input_, location):
    grid, start_location = input_
    lx, ly = location
    grid = deepcopy(grid)
    grid[lx][ly] = "#"

    try:
        find_original_path(grid, start_location)
        return False
    except LoopException:
        return True


def main2(input_):
    grid, start_location = input_
    seen_locations = find_original_path(grid, start_location)
    seen_locations.remove(start_location)
    return sum(is_loop_with_obstacle(input_, location) for location in seen_locations)
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
