from copy import deepcopy
import sys


def parse_input(input):
    return [[v == "#" for v in row.rstrip()] for row in input]


def get_grid(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid):
        return False
    return grid[i][j]


def count_on_neighbours(grid, i, j):
    return (
        get_grid(grid, i - 1, j - 1)
        + get_grid(grid, i - 1, j)
        + get_grid(grid, i - 1, j + 1)
        + get_grid(grid, i, j - 1)
        + get_grid(grid, i, j + 1)
        + get_grid(grid, i + 1, j - 1)
        + get_grid(grid, i + 1, j)
        + get_grid(grid, i + 1, j + 1)
    )


STEPS = 100


def main1(input):
    grid = parse_input(input)
    for _ in range(STEPS):
        new_grid = deepcopy(grid)
        for i, row in enumerate(grid):
            for j in range(len(row)):
                current = grid[i][j]
                on_neighbours = count_on_neighbours(grid, i, j)
                new_grid[i][j] = (current and on_neighbours in (2, 3)) or (
                    not current and on_neighbours == 3
                )
        grid = new_grid
    return sum(v for row in grid for v in row)


def main2(input):
    grid = parse_input(input)
    grid[0][-1] = True
    grid[-1][-1] = True
    grid[0][0] = True
    grid[-1][0] = True
    for _ in range(STEPS):
        new_grid = deepcopy(grid)
        for i, row in enumerate(grid):
            for j in range(len(row)):
                current = grid[i][j]
                on_neighbours = count_on_neighbours(grid, i, j)
                new_grid[i][j] = (current and on_neighbours in (2, 3)) or (
                    not current and on_neighbours == 3
                )
        grid = new_grid
        grid[0][-1] = True
        grid[-1][-1] = True
        grid[0][0] = True
        grid[-1][0] = True
    return sum(v for row in grid for v in row)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
