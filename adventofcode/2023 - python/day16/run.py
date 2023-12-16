import sys
from enum import Enum, auto
from pathlib import Path
from telnetlib import DO
from tkinter import LEFT


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


flow = {
    "-": {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    },
    "|": {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    },
    "/": {
        Direction.UP: [Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT],
        Direction.LEFT: [Direction.DOWN],
        Direction.RIGHT: [Direction.UP],
    },
    "\\": {
        Direction.UP: [Direction.LEFT],
        Direction.DOWN: [Direction.RIGHT],
        Direction.LEFT: [Direction.UP],
        Direction.RIGHT: [Direction.DOWN],
    },
    ".": {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    },
}

coord_deltas = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def main1(input_, start=(0, -1), start_direction=Direction.RIGHT):
    height = len(input_)
    width = len(input_[0])

    energy_direction = {
        direction: [[False] * width for _ in range(height)] for direction in Direction
    }
    sys.setrecursionlimit(100_000)

    def follow_through(coord, direction):
        delta_x, delta_y = coord_deltas[direction]
        x, y = coord[0] + delta_x, coord[1] + delta_y

        if x < 0 or y < 0 or x >= height or y >= width:
            return

        if energy_direction[direction][x][y]:
            # already passed in this direction
            return
        energy_direction[direction][x][y] = True
        for new_direction in flow[input_[x][y]][direction]:
            follow_through((x, y), new_direction)

    follow_through(start, start_direction)

    return sum(
        any(energy_direction[direction][x][y] for direction in Direction)
        for x in range(height)
        for y in range(width)
    )


def main2(input_):
    height = len(input_)
    width = len(input_[0])
    return max(
        (
            *(main1(input_, (i, -1), Direction.RIGHT) for i in range(height)),
            *(main1(input_, (i, width), Direction.LEFT) for i in range(height)),
            *(main1(input_, (-1, i), Direction.DOWN) for i in range(width)),
            *(main1(input_, (height, i), Direction.UP) for i in range(width)),
        )
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
