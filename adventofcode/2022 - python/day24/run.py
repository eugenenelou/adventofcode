import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

DIRECTION_STRINGS = (">", "v", "<", "^")
DIRECTION_DELTAS = ((0, 1), (1, 0), (0, -1), (-1, 0))
MY_OPTIONS = ((-1, 0), (0, -1), (0, 0), (1, 0), (0, 1))


class Direction(int, Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    @classmethod
    def from_string(cls, value):
        return cls(DIRECTION_STRINGS.index(value))

    @property
    def delta(self):
        return DIRECTION_DELTAS[self]


def translate(a, b):
    return a[0] + b[0], a[1] + b[1]


@dataclass(frozen=True, slots=True)
class Blizzard:
    x: int
    y: int
    direction: Direction

    def move(self, height, width):
        x, y = translate((self.x, self.y), self.direction.delta)
        # No need to handle the entrance/exit blizzards are trapped
        x = 1 + (x - 1) % (height - 2)
        y = 1 + (y - 1) % (width - 2)
        return Blizzard(x=x, y=y, direction=self.direction)


def parse_input():
    input_filepath = sys.argv[1]
    p = Path(input_filepath)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    blizzards = set()
    grid = []
    for x, line in enumerate(content.split("\n")):
        row = []
        for y, char in enumerate(line):
            if char == "#":
                row.append(False)
            else:
                row.append(True)
                if char != ".":
                    blizzards.add(
                        Blizzard(x=x, y=y, direction=Direction.from_string(char))
                    )
        grid.append(row)
    return grid, blizzards


def display(grid, blizzards):
    d = [["." if value else "#" for value in row] for row in grid]
    for b in blizzards:
        d[b.x][b.y] = DIRECTION_STRINGS[b.direction]
    for row in d:
        print("".join(row))


def main1():
    grid, blizzards = parse_input()
    height, width = len(grid), len(grid[0])
    positions = [(0, next(y for y, value in enumerate(grid[0]) if value))]
    target = (height - 1, next(y for y, value in enumerate(grid[-1]) if value))

    t = 0
    print("Start")
    display(grid, blizzards)
    while True:
        t += 1
        blizzards = {blizzard.move(height, width) for blizzard in blizzards}
        blizzard_pos = {(b.x, b.y) for b in blizzards}
        new_positions = set()
        for position in positions:
            for delta in MY_OPTIONS:
                pos = translate(position, delta)
                if not grid[pos[0]][pos[1]]:
                    continue
                if pos == target:
                    return t
                if pos not in blizzard_pos:
                    new_positions.add(pos)
        positions = new_positions


def is_valid(x, y, grid, height, width):
    return 0 <= x < height and 0 <= y < width and grid[x][y]


def main2():
    grid, blizzards = parse_input()
    height, width = len(grid), len(grid[0])
    entrance = (0, next(y for y, value in enumerate(grid[0]) if value))
    exit_ = (height - 1, next(y for y, value in enumerate(grid[-1]) if value))
    positions_1 = [entrance]  # first trip
    positions_2 = []  # second trip
    positions_3 = []  # third trip

    t = 0
    print("Start")
    display(grid, blizzards)
    while True:
        t += 1
        blizzards = {blizzard.move(height, width) for blizzard in blizzards}
        blizzard_pos = {(b.x, b.y) for b in blizzards}
        new_positions_1 = set()
        new_positions_2 = set()
        new_positions_3 = set()
        for position in positions_1:
            for delta in MY_OPTIONS:
                pos = translate(position, delta)
                if not is_valid(pos[0], pos[1], grid, height, width):
                    continue
                if pos == exit_:
                    new_positions_2.add(pos)
                elif pos not in blizzard_pos:
                    new_positions_1.add(pos)
        for position in positions_2:
            for delta in MY_OPTIONS:
                pos = translate(position, delta)
                if not is_valid(pos[0], pos[1], grid, height, width):
                    continue
                if pos == entrance:
                    new_positions_3.add(pos)
                elif pos not in blizzard_pos:
                    new_positions_2.add(pos)
        for position in positions_3:
            for delta in MY_OPTIONS:
                pos = translate(position, delta)
                if not is_valid(pos[0], pos[1], grid, height, width):
                    continue
                if pos == exit_:
                    return t
                if pos not in blizzard_pos:
                    new_positions_3.add(pos)
        positions_1 = new_positions_1
        positions_2 = new_positions_2
        positions_3 = new_positions_3


if __name__ == "__main__":
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    print(f"result: {main2() if second_part else main1()}", file=sys.stdout)
