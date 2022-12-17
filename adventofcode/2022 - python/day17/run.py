import sys
from pathlib import Path
from dataclasses import dataclass
from itertools import cycle
from typing import Sequence

from functools import cached_property


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [direction == ">" for direction in content]


# ordered by estimated colliding probability
piece_templates = [
    ((0, 1), (0, 0), (0, 2), (0, 3)),
    ((0, 1), (1, 1), (1, 0), (1, 2), (2, 1)),
    ((0, 1), (0, 0), (0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 1), (0, 0), (1, 1), (1, 0)),
]

WIDTH = 7


@dataclass
class Piece:
    x: int
    y: int
    blocks: Sequence[tuple[int, int]]

    @cached_property
    def width(self):
        return max(y for _, y in self.blocks) + 1

    @cached_property
    def height(self):
        return max(x for x, _ in self.blocks) + 1

    def move(self, direction, grid):
        if direction:
            if self.y + self.width < WIDTH:
                self.y += 1
                if self.overlap(grid):
                    self.y -= 1
        else:
            if self.y > 0:
                self.y -= 1
                if self.overlap(grid):
                    self.y += 1

    def overlap(self, grid):
        n = len(grid)
        for x, y in self.blocks:
            if (self.x + x) < n and grid[self.x + x][self.y + y]:
                return True
        return False


def print_grid(grid):
    for row in grid[::-1]:
        print("".join("#" if block else "." for block in row))


def get_profile(grid):
    profile = [None] * WIDTH
    found = 0
    n = len(grid)
    for i in range(n - 1, 0 - 1, -1):
        for j, block in enumerate(grid[i]):
            if profile[j] is None and block:
                profile[j] = n - 1 - i
                found += 1
                if found == WIDTH:
                    break
    return tuple(profile)


def main(input_, n_blocks):
    grid = [[True] * WIDTH]
    n_dirs = len(input_)

    found_configurations = {}

    def draw_piece(piece: Piece):
        for _ in range(len(grid), piece.x + piece.height):
            grid.extend([[False] * WIDTH])
        for x, y in piece.blocks:
            grid[piece.x + x][piece.y + y] = True

    dir_idx = 0
    i = -1
    cycle_found = False
    grid_len_when_cycle_found = None
    result = None
    for template in cycle(piece_templates):
        i += 1
        if i >= n_blocks:
            break

        piece = Piece(x=len(grid) + 3, y=2, blocks=template)
        while not piece.overlap(grid):
            direction = input_[dir_idx % n_dirs]
            dir_idx += 1
            piece.move(direction, grid)
            piece.x -= 1
        piece.x += 1
        draw_piece(piece)

        configuration = (get_profile(grid), dir_idx % n_dirs)
        if not cycle_found:
            if config := found_configurations.get(configuration):
                cycle_found = True
                j, block_layers = config
                cycle_length = i - j
                grid_len_when_cycle_found = len_grid = len(grid)
                cycle_block_layers = len_grid - block_layers
                remaining_cycles = (n_blocks - i - 1) // cycle_length
                result = len_grid + cycle_block_layers * remaining_cycles
                i += cycle_length * remaining_cycles
            else:
                found_configurations[configuration] = (i, len(grid))

    return result + len(grid) - grid_len_when_cycle_found - 1  # minus one for the bottom layer


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main(input_, n_blocks=int(1e12))}", file=sys.stdout)
    else:
        print(f"result: {main(input_, n_blocks=2022)}", file=sys.stdout)
