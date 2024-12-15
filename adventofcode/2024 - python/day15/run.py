import sys
from itertools import chain
from pathlib import Path

DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_grid, raw_instructions = content.split("\n\n")

    grid = []
    for i, raw_line in enumerate(raw_grid.split("\n")):
        line = []
        grid.append(line)
        for j, char in enumerate(raw_line):
            if char == "@":
                start_pos = (i, j)
                char = "."
            line.append(char)

    instructions = []
    for raw_instruction in chain(*raw_instructions.split("\n")):
        instructions.append(DIRECTIONS[raw_instruction])
    return start_pos, grid, instructions


def get_gps_coord(x, y):
    return 100 * x + y


def display(grid, robot):
    grid = grid.copy()
    grid[robot[0]] = grid[robot[0]].copy()
    grid[robot[0]][robot[1]] = "@"
    for line in grid:
        print("".join(line))


def main1(input_):
    (rx, ry), grid, instructions = input_
    for dx, dy in instructions:
        moved_block = False
        moved = False
        x = rx + dx
        y = ry + dy
        cell = grid[x][y]
        while True:
            match cell:
                case ".":
                    moved = True
                    if moved_block:
                        grid[x][y] = "O"
                        grid[rx + dx][ry + dy] = "."
                    break
                case "#":
                    break
                case _:  # case "O"
                    moved_block = True
            x += dx
            y += dy
            cell = grid[x][y]
        if moved:
            rx += dx
            ry += dy
        # print("\n", (dx, dy))
        # display(grid, (rx, ry))

    return sum(
        get_gps_coord(x, y)
        for x, line in enumerate(grid)
        for y, char in enumerate(line)
        if char == "O"
    )


def convert_to_wider_grid(input_):
    (rx, raw_ry), raw_grid, instructions = input_
    ry = raw_ry * 2
    grid = []
    for raw_line in raw_grid:
        line = []
        for char in raw_line:
            match char:
                case "#":
                    line.append("#")
                    line.append("#")
                case ".":
                    line.append(".")
                    line.append(".")
                case "O":
                    line.append("[")
                    line.append("]")
        grid.append(line)
    return (rx, ry), grid, instructions


def main2(input_):
    (rx, ry), grid, instructions = convert_to_wider_grid(input_)

    def check_can_move(x, y, dx):
        match grid[x + dx][y]:
            case ".":
                return True
            case "#":
                return False
            case "[":
                return check_can_move(x + dx, y, dx) and check_can_move(
                    x + dx, y + 1, dx
                )
            case "]":
                return check_can_move(x + dx, y, dx) and check_can_move(
                    x + dx, y - 1, dx
                )

    already_moved = set()

    def move_vertically(x, y, dx):
        # recursively move blocks, then the current block
        if (x, y) in already_moved:
            return
        already_moved.add((x, y))
        match grid[x][y]:
            case "[":
                move_vertically(x + dx, y, dx)
                move_vertically(x + dx, y + 1, dx)
                grid[x + dx][y] = "["
                grid[x][y] = "."
                already_moved.add((x, y + 1))
                grid[x + dx][y + 1] = "]"
                grid[x][y + 1] = "."
            case "]":
                move_vertically(x + dx, y, dx)
                move_vertically(x + dx, y - 1, dx)
                grid[x + dx][y] = "]"
                grid[x][y] = "."
                already_moved.add((x, y - 1))
                grid[x + dx][y - 1] = "["
                grid[x][y - 1] = "."

    for dx, dy in instructions:
        if dx == 0:  # move horizontally
            x = rx + dx
            y = ry + dy
            cell = grid[x][y]
            can_move = False
            line = grid[x]
            cell = line[y]
            i = 0
            while True:
                i += 1
                if cell == ".":
                    can_move = True
                    break
                if cell == "#":
                    break
                y += dy
                cell = line[y]
            if can_move:
                y = ry = ry + dy
                line[y] = "."
                moved_block = False
                for _ in range(i - 1):
                    y += dy
                    match line[y]:
                        case "[":
                            moved_block = True
                            line[y] = "]"
                        case "]":
                            moved_block = True
                            line[y] = "["
                if moved_block:
                    line[y] = "]" if dy > 0 else "["
        else:  # move vertically
            can_move = check_can_move(rx, ry, dx)
            if can_move:
                move_vertically(rx + dx, ry, dx)
                already_moved = set()
                rx += dx

        # print("\n", (dx, dy))
        # display(grid, (rx, ry))

    return sum(
        get_gps_coord(x, y)
        for x, line in enumerate(grid)
        for y, char in enumerate(line)
        if char == "["
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
