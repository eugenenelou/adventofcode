from dataclasses import dataclass, field
import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


@dataclass
class Area:
    idx: int
    char: str
    cells: set[tuple[int, int]] = field(default_factory=set)
    perimeter: int = 0
    sides: int = 0

    def find_neighbors(self, x, y, char, grid):
        cells = self.cells
        cells.add((x, y))
        self.perimeter = 4
        H, W = len(grid), len(grid[0])

        def inner(x, y):
            for dx, dy in DIRECTIONS:
                new_x = x + dx
                new_y = y + dy

                if 0 <= new_x < H and 0 <= new_y < W and grid[new_x][new_y] == char:
                    self.perimeter -= 1
                    if (new_x, new_y) not in cells:
                        cells.add((new_x, new_y))
                        self.perimeter += 4
                        inner(new_x, new_y)

        inner(x, y)

    def get_sides(self, grid):
        H, W = len(grid), len(grid[0])
        sides = 0
        for x, y in self.cells:
            top = 0 < x and grid[x - 1][y] == self.char
            top_left = 0 < x and 0 < y and grid[x - 1][y - 1] == self.char
            left = 0 < y and grid[x][y - 1] == self.char
            # count the left sides
            if (not left) and (not top or top_left):
                sides += 1
            # count the top sides
            if (not top) and (not left or top_left):
                sides += 1

            bottom = x < H - 1 and grid[x + 1][y] == self.char
            bottom_right = (
                (x < H - 1) and (y < W - 1) and grid[x + 1][y + 1] == self.char
            )
            right = y < W - 1 and grid[x][y + 1] == self.char
            # count the right sides
            if (not right) and (not bottom or bottom_right):
                sides += 1
            # count the bottom sides
            if (not bottom) and (not right or bottom_right):
                sides += 1
        return sides


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def map_areas(input_):
    H, W = len(input_), len(input_[0])
    mapped = [[-1] * W for _ in range(H)]
    areas = []

    for x, line in enumerate(input_):
        for y, char in enumerate(line):
            if mapped[x][y] != -1:
                continue
            idx = len(areas)
            area = Area(idx=idx, char=char)
            areas.append(area)
            area.find_neighbors(x, y, char, input_)
            for cX, cY in area.cells:
                mapped[cX][cY] = idx
    return areas


def main1(input_):
    areas = map_areas(input_)
    return sum(area.perimeter * len(area.cells) for area in areas)


def main2(input_):
    areas = map_areas(input_)
    return sum(area.get_sides(input_) * len(area.cells) for area in areas)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
