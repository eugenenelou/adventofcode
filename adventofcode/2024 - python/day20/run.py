from functools import cache, lru_cache
import sys
from pathlib import Path


# copied from day16
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


def get_cost_by_cell_without_cheat(grid, end) -> dict[tuple[int, int], int]:
    H = len(grid)
    W = len(grid[0])
    cost_by_cell = {end: 0}
    next_pos = [end]
    i = 0
    while len(next_pos) > 0:
        i += 1
        new_next_pos = set()
        for pos in next_pos:
            for dx, dy in DIRECTIONS:
                new_x = pos[0] + dx
                new_y = pos[1] + dy
                if (
                    new_x < 0
                    or new_y < 0
                    or new_x >= H
                    or new_y >= W
                    or (new_x, new_y) in cost_by_cell
                    or not grid[new_x][new_y]
                ):
                    continue
                cost_by_cell[(new_x, new_y)] = i
                new_next_pos.add((new_x, new_y))
        next_pos = new_next_pos
    return cost_by_cell


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def main1(input_, threshold=100):
    grid, start, end = input_

    cost_by_cell_without_cheat = get_cost_by_cell_without_cheat(grid, end)
    no_cheat_best = cost_by_cell_without_cheat[start]

    time_saved_by_cheat = {}

    next_pos = [start]
    reached_pos = set()
    i = 0
    H = len(grid)
    W = len(grid[0])
    while len(next_pos) > 0:
        i += 1
        new_next_pos = []
        for pos in next_pos:
            if i + manhattan(pos, end) > no_cheat_best:
                continue

            # possible cheats are only walls the track behind
            x, y = pos
            for dir_idx, (dx, dy) in enumerate(DIRECTIONS):
                new_x = x + dx
                new_y = y + dy
                if new_x < 0 or new_y < 0 or new_x >= H or new_y >= W:
                    continue
                if grid[new_x][new_y]:
                    if (new_x, new_y) not in reached_pos:
                        reached_pos.add((new_x, new_y))
                        new_next_pos.append((new_x, new_y))
                else:
                    for j in range(-1, 2):
                        dx2, dy2 = DIRECTIONS[(dir_idx + j) % 4]
                        new_x2 = new_x + dx2
                        new_y2 = new_y + dy2
                        if new_x2 < 0 or new_y2 < 0 or new_x2 >= H or new_y2 >= W:
                            continue
                        if grid[new_x2][new_y2]:
                            gain = no_cheat_best - (
                                i + 1 + cost_by_cell_without_cheat[(new_x2, new_y2)]
                            )
                            if gain >= threshold:
                                time_saved_by_cheat[(x, y, new_x, new_y)] = gain
        next_pos = new_next_pos

    return len(time_saved_by_cheat.values())


def main2(input_, threshold=100):
    grid, start, end = input_
    H = len(grid)
    W = len(grid[0])

    cost_from_end = get_cost_by_cell_without_cheat(grid, end)
    cost_from_end_grid = [[None] * W for _ in range(H)]
    for (x, y), cost in cost_from_end.items():
        cost_from_end_grid[x][y] = cost
    cost_from_start = get_cost_by_cell_without_cheat(grid, start)
    
    no_cheat_best = cost_from_end[start]

    # we need to find all the pair of coordinates where from_start[a] - from_start[b] >= 100
    # and manhattan(a, b) <= 20
    

    time_saved_by_cheat = {}

    next_pos = [start]
    reached_pos = set()
    i = 0
    while len(next_pos) > 0:
        i += 1
        new_next_pos = []
        for pos in next_pos:
            if i + manhattan(pos, end) > no_cheat_best - threshold:
                continue
                # check only the perimeter

            # possible cheats are only walls the track behind
            x, y = pos
            for dir_idx, (dx, dy) in enumerate(DIRECTIONS):
                new_x = x + dx
                new_y = y + dy
                if new_x < 0 or new_y < 0 or new_x >= H or new_y >= W:
                    continue
                if grid[new_x][new_y]:
        next_pos = new_next_pos

    return len(time_saved_by_cheat.values())


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
