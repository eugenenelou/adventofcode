import sys
from pathlib import Path
from string import ascii_letters

letter_value = {l: i for i, l in enumerate(ascii_letters)}
letter_value["S"] = letter_value["a"]
letter_value["E"] = letter_value["z"]


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    grid = []
    for i, line in enumerate(content.split("\n")):
        row = []
        for j, cell in enumerate(line):
            if cell == "S":
                start = (i, j)
            elif cell == "E":
                end = (i, j)
            row.append(letter_value[cell])
        grid.append(row)
    return grid, start, end


def is_valid_step(v_from, v_to, reverse=False):
    diff = v_to - v_from
    return (-diff if reverse else diff) <= 1


def main1(input_):
    grid, start, end = input_
    visited = {start}

    print(f"{start=}, {end=}")
    for r in grid:
        print(".".join(map(str, r)))

    n = len(grid)
    m = len(grid[0])

    def get_next_cells(cell, reverse=True):
        x, y = cell
        value = grid[x][y]
        if x > 0:
            next_cell = (x - 1, y)
            if next_cell not in visited and grid[x - 1][y] - value <= 1:
                yield next_cell
        if y > 0:
            next_cell = (x, y - 1)
            if next_cell not in visited and grid[x][y - 1] - value <= 1:
                yield next_cell
        if x < n - 1:
            next_cell = (x + 1, y)
            if next_cell not in visited and grid[x + 1][y] - value <= 1:
                yield next_cell
        if y < m - 1:
            next_cell = (x, y + 1)
            if next_cell not in visited and grid[x][y + 1] - value <= 1:
                yield next_cell

    i = 0
    result = None
    cells_to_visit = [start]
    while cells_to_visit:
        i += 1
        next_cells = []
        for cell in cells_to_visit:
            for next_cell in get_next_cells(cell):
                if next_cell == end:
                    result = i
                    break
                visited.add(next_cell)
                next_cells.append(next_cell)
        cells_to_visit = next_cells
    return result


def main2(input_):
    """same but start from E"""
    grid, start, end = input_
    end, start = start, end
    visited = {start}

    print(f"{start=}, {end=}")
    for r in grid:
        print(".".join(map(str, r)))

    n = len(grid)
    m = len(grid[0])

    def get_next_cells(cell, reverse=False):
        x, y = cell
        value = grid[x][y]
        if x > 0:
            next_cell = (x - 1, y)
            if next_cell not in visited and is_valid_step(value, grid[x - 1][y], reverse=reverse):
                yield next_cell
        if y > 0:
            next_cell = (x, y - 1)
            if next_cell not in visited and is_valid_step(value, grid[x][y - 1], reverse=reverse):
                yield next_cell
        if x < n - 1:
            next_cell = (x + 1, y)
            if next_cell not in visited and is_valid_step(value, grid[x + 1][y], reverse=reverse):
                yield next_cell
        if y < m - 1:
            next_cell = (x, y + 1)
            if next_cell not in visited and is_valid_step(value, grid[x][y + 1], reverse=reverse):
                yield next_cell

    i = 0
    cells_to_visit = [start]
    while cells_to_visit:
        i += 1
        next_cells = []
        for cell in cells_to_visit:
            for next_cell in get_next_cells(cell, reverse=True):
                x, y = next_cell
                if grid[x][y] == 0:
                    print("start: ", next_cell)
                    return i
                visited.add(next_cell)
                next_cells.append(next_cell)
        cells_to_visit = next_cells
    raise ValueError


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
