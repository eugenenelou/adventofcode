import bisect
from collections import defaultdict
from operator import itemgetter
from pickle import NEWOBJ_EX
import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    grid = []
    for x, raw_line in enumerate(content.split("\n")):
        grid.append(line := [])
        for y, cell in enumerate(raw_line):
            if cell == "#":
                line.append(False)
            else:
                line.append(True)
                if cell == "E":
                    end = (x, y)
                elif cell == "S":
                    start = (x, y)
    return grid, start, end


DIRECTIONS = [NORTH := (-1, 0), WEST := (0, -1), SOUTH := (1, 0), EAST := (0, 1)]

get_cost = itemgetter(2)


def main1(input_):
    grid, start, (end_x, end_y) = input_
    reached_positions = {start: 0}
    states = [(start, EAST, 0)]

    min_exit_cost = None

    i = 0
    while True:
        i += 1
        (x, y), (state_dx, state_dy), cost = states.pop(0)
        if min_exit_cost is not None and cost > min_exit_cost:
            return min_exit_cost
        for dx, dy in DIRECTIONS:
            new_x = x + dx
            new_y = y + dy
            if not grid[new_x][new_y]:
                continue
            new_cost = cost + (1001 if (dx == 0) != (state_dx == 0) else 1)

            if new_x == end_x and new_y == end_y:
                if min_exit_cost is None or new_cost < min_exit_cost:
                    min_exit_cost = new_cost
            else:
                old_cost = reached_positions.get((new_x, new_y))
                if old_cost is None or new_cost < old_cost:
                    reached_positions[(new_x, new_y)] = new_cost
                    bisect.insort(
                        states, ((new_x, new_y), (dx, dy), new_cost), key=get_cost
                    )


def main2(input_):
    grid, start, (end_x, end_y) = input_
    reached_positions = {start: 0}
    states = [(start, EAST, 0, [start])]

    min_exit_cost = None
    path_reaching_exit_by_cost = defaultdict(set)

    while True:
        (x, y), (state_dx, state_dy), cost, path = states.pop(0)
        if min_exit_cost is not None and cost > min_exit_cost:
            break
        for dx, dy in DIRECTIONS:
            new_x = x + dx
            new_y = y + dy
            if not grid[new_x][new_y]:
                continue
            new_cost = cost + (1001 if (dx == 0) != (state_dx == 0) else 1)

            if new_x == end_x and new_y == end_y:
                path_reaching_exit_by_cost[new_cost].update(path)
                if min_exit_cost is None or new_cost < min_exit_cost:
                    min_exit_cost = new_cost
            else:
                old_cost = reached_positions.get((new_x, new_y))
                if (
                    old_cost is None
                    or new_cost <= old_cost
                    or new_cost == old_cost + 1000
                    # this does not discard the path in case the next path of the already
                    # found one would use a direction change (+1000) but not the current
                    # one, ending in the same total cost. Using an inequality instead of the
                    # equality does not work as it explodes in algorithmic complexity.
                ):
                    reached_positions[(new_x, new_y)] = new_cost
                    bisect.insort(
                        states,
                        ((new_x, new_y), (dx, dy), new_cost, [*path, (new_x, new_y)]),
                        key=get_cost,
                    )

    best_paths = path_reaching_exit_by_cost[min_exit_cost]
    for x, line in enumerate(grid):
        print(
            "".join(
                "#" if not cell else ("O" if (x, y) in best_paths else ".")
                for y, cell in enumerate(line)
            )
        )
    return len(path_reaching_exit_by_cost[min_exit_cost]) + 1


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
