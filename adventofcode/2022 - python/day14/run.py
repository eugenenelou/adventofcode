import sys
from pathlib import Path


def get_dir(from_, to):
    dx = to[0] - from_[0]
    dy = to[1] - from_[1]
    return dx / (abs(dx) if dx else 1), dy / (abs(dy) if dy else 1)


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    minX, minY, maxX, maxY = 500, 500, 0, 0
    paths = []
    for line in content.split("\n"):
        path = []
        paths.append(path)
        for point in line.split(" -> "):
            x, y = map(int, point.split(","))
            if x > maxX:
                maxX = x
            if x < minX:
                minX = x
            if y > maxY:
                maxY = y
            if y < minY:
                minY = y
            path.append((x, y))

    offsetX = minX - 2

    grid = [["." for _ in range(maxY + 1)] for _ in range(maxX + 1 - offsetX)]
    for path in paths:
        for from_, to in zip(path[:-1], path[1:]):
            dir_ = get_dir(from_, to)
            print("dir ", dir_)
            if dir_ == (0, 1):
                grid[from_[0] - offsetX][from_[1] : to[1] + 1] = ["#"] * (to[1] + 1 - from_[1])
            if dir_ == (0, -1):
                grid[from_[0] - offsetX][to[1] : from_[1] + 1] = ["#"] * (from_[1] + 1 - to[1])
            elif dir_ == (1, 0):
                for x in range(from_[0], to[0] + 1):
                    grid[x - offsetX][from_[1]] = "#"
            elif dir_ == (-1, 0):
                for x in range(to[0], from_[0] + 1):
                    grid[x - offsetX][from_[1]] = "#"
    return grid, (500 - offsetX, 0)


def main1(grid, input_):
    for line in grid:
        print("".join(line))

    n, m = len(grid), len(grid[0])
    # store the next place to send a sand block
    # grid_next_sand = [[None for _ in range(m)] for _ in range(n)]

    def get_next_sand_direct(point):
        x, y = point
        if x + 1 < n and grid[x + 1][y] == ".":
            return (x, y + 1)
        if y - 1 >= 0 and x + 1 < n and grid[x + 1][y - 1] == ".":
            return (x + 1, y - 1)
        if y + 1 < m and x + 1 < n and grid[x + 1][y + 1] == ".":
            return (x + 1, y + 1)
        # if y - 1 >= 0 and grid[x][y - 1] == ".":
        #     return (x, y - 1)
        # if y + 1 < m and grid[x][y + 1] == ".":
        #     return (x, y + 1)
        return False

    def get_next_sand(point):
        next_ = point
        last_point = False
        while next_ := get_next_sand_direct(next_):
            last_point = next_
        return last_point

    result = 0
    while next_sand := get_next_sand(input_):
        result += 1
        x, y = next_sand
        grid[x][y] = "o"

    for line in grid:
        print("".join(line))
    return result


def main2(grid, input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(*input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(*input_)}", file=sys.stdout)
