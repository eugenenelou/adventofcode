import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_grid = content.split("\n")
    s = next(
        (x, y)
        for x, row in enumerate(raw_grid)
        for y, char in enumerate(row)
        if char == "S"
    )
    return s, [[char != "#" for char in row] for row in raw_grid]


DELTAS = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def count_tiles(grid, start, steps=64):
    height, width = len(grid), len(grid[0])
    positions = [start]
    reached_positions = {start}
    # print("start", start)

    counts_per_step = [1]
    for _ in range(steps):
        reached_positions_for_step = set()
        new_positions = []
        for px, py in positions:
            for dx, dy in DELTAS:
                x = px + dx
                y = py + dy
                if not (
                    x < 0
                    or y < 0
                    or x >= height
                    or y >= width
                    or not grid[x][y]
                    or (x, y) in reached_positions
                ):
                    new_positions.append((x, y))
                    reached_positions.add((x, y))
                    reached_positions_for_step.add((x, y))
        positions = new_positions
        # print("reached_positions_for_step", reached_positions_for_step)
        counts_per_step.append(len(reached_positions_for_step))
    # print(sum(counts_per_step))
    return sum(count for count in counts_per_step[steps % 2 :: 2])


def main1(input_):
    start, grid = input_
    return count_tiles(grid, start)


STEPS = 26501365


def main2(input_):
    """
    in the pattern the row and column of the start are empty
    the start is in the middle and the pattern is square.
    And all the edges are empty, so reaching a tile on the edge of any pattern
    is always the manhattan distance from the start.
    There is algo a diamond shape in the pattern that is empty, this
    is where we reach at the edge of the STEPS because STEPS % edge is edge/2.
    when reaching a pattern, the parity of the cases reached is inverted,
    so The final number of tiles reached is the total number of tiles minus the walls
    and halved.

    let N be the the quotient of steps divided by the size of the pattern

    The number of pattern fully traversed that end up on an ODD tile (as seen from the start)
    increase in a logical suite with the number of steps:  1 + 4N((N-1)//2)((N-1//2)+1)
    The number of pattern fully traversed that end up on an EVEN tile (as seen from the start)
    increase in a logical suite with the number of steps:  4(N//2)^2

    There are one of each pattern of the form:
    ##.  ###  .##  .#.
    ###  ###  ###  ###
    ##.  .#.  .##  ###

    There are N pattern of each form:
    ...  ...  #..  ..#
    ...  ...  ...  ...
    ..#  #..  ...  ...

    And there are N-1 pattern of each form:
    ##.  ###  ###  .##
    ###  ###  ###  ###
    ###  ##.  .##  ###
    """
    start, grid = input_
    height, width = len(grid), len(grid[0])
    assert height == width
    assert height % 2 == 1

    half = height // 2
    full_pattern_odd = count_tiles(grid, start, 2 * half + 1)
    full_pattern_even = count_tiles(grid, start, 2 * half)

    N = STEPS // height
    assert N % 2 == 0
    assert (STEPS % height) == half
    number_of_full_patterns_odd = 1 + 4 * ((N - 1) // 2) * ((N - 1) // 2 + 1)
    number_of_full_patterns_even = 4 * (N // 2) ** 2
    total_full_pattern_odd = number_of_full_patterns_odd * full_pattern_odd
    total_full_pattern_even = number_of_full_patterns_even * full_pattern_even

    return (
        total_full_pattern_odd
        + total_full_pattern_even
        # just corner
        + N
        * (
            count_tiles(grid, (0, 0), half - 1)
            + count_tiles(grid, (0, height - 1), half - 1)
            + count_tiles(grid, (height - 1, height - 1), half - 1)
            + count_tiles(grid, (height - 1, 0), half - 1)
        )
        # missing corner
        + (N - 1)
        * (
            count_tiles(grid, (0, 0), 3 * half)
            + count_tiles(grid, (0, height - 1), 3 * half)
            + count_tiles(grid, (height - 1, height - 1), 3 * half)
            + count_tiles(grid, (height - 1, 0), 3 * half)
        )
        # missing 2 corners
        + count_tiles(grid, (0, half), 2 * half)
        + count_tiles(grid, (height - 1, half), 2 * half)
        + count_tiles(grid, (half, 0), 2 * half)
        + count_tiles(grid, (half, height - 1), 2 * half)
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
