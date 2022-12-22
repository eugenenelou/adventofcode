import sys
from pathlib import Path
import re
from dataclasses import dataclass


@dataclass
class Grid:
    rows: list[str]
    offsets: list[int]


def get_next_dir(current_dir: int, turn: str):
    return (current_dir + (-1 if turn == "L" else 1)) % 4


def parse_instructions(instructions: str) -> list[str | int]:
    directions = []
    for instruction in re.split(
        "(L|R)",
        instructions,
    ):
        if instruction == "L" or instruction == "R":
            directions.append(instruction)
        elif instruction:
            directions.append(int(instruction))
    return directions


def parse_input1(path: str):
    p = Path(path)
    content, instructions = p.read_text().split("\n\n")
    content = re.sub(r"\n$", "", content).split("\n")

    grid_hori = Grid(rows=[], offsets=[])
    for line in content:
        offset = 0
        n = len(line)
        line = line.lstrip()
        offset = n - len(line)
        grid_hori.rows.append(line.rstrip())
        grid_hori.offsets.append(offset)

    grid_verti = Grid(rows=[], offsets=[])
    m = max(len(line) for line in content)
    for i in range(m):
        offset = 0
        row = []
        found_start = False
        for line in content:
            elt = line[i] if i < len(line) else " "
            match (elt, found_start):
                case " ", True:
                    break
                case " ", False:
                    offset += 1
                case a, _:
                    found_start = True
                    row.append(a)
        grid_verti.rows.append("".join(row))
        grid_verti.offsets.append(offset)

    return grid_hori, grid_verti, parse_instructions(instructions)


def main1(grid_hori, grid_verti, directions):
    x, y = 0, grid_hori.offsets[0]
    current_dir = 0
    print(f"{x=}, {y=}, {current_dir=}")
    for direction in directions:
        if isinstance(direction, int):
            match current_dir:
                case 0:
                    offset = grid_hori.offsets[x]
                    row = grid_hori.rows[x]
                    new_y = y
                    for i in range(1, direction + 1):
                        row_idx = (y - offset + i) % len(row)
                        if row[row_idx] == "#":
                            break
                        new_y = offset + row_idx
                    y = new_y
                case 2:
                    offset = grid_hori.offsets[x]
                    row = grid_hori.rows[x]
                    new_y = y
                    for i in range(1, direction + 1):
                        row_idx = (y - offset - i) % len(row)
                        if row[row_idx] == "#":
                            break
                        new_y = offset + row_idx
                    y = new_y
                case 1:
                    offset = grid_verti.offsets[y]
                    row = grid_verti.rows[y]
                    new_x = x
                    for i in range(1, direction + 1):
                        row_idx = (x - offset + i) % len(row)
                        print(f"{row_idx=}", new_x)
                        if row[row_idx] == "#":
                            break
                        new_x = offset + row_idx
                    x = new_x
                case 3:
                    offset = grid_verti.offsets[y]
                    row = grid_verti.rows[y]
                    new_x = x
                    for i in range(1, direction + 1):
                        row_idx = (x - offset - i) % len(row)
                        if row[row_idx] == "#":
                            break
                        new_x = offset + row_idx
                    x = new_x
        else:
            current_dir = get_next_dir(current_dir, direction)
        print(f"{direction=}, {x=}, {y=}, {current_dir=}")
    return 1000 * (x + 1) + 4 * (y + 1) + current_dir


# __1
# 234
# __56
N = 4
face_locations = [[None, None, 1, None], [2, 3, 4, None], [None, None, 5, 6]]
# (face, direction) -> (face_direction)
transitions = {
    (1, 0): (6, 2),
    (1, 1): (4, 1),
    (1, 2): (3, 1),
    (1, 3): (2, 1),
    (2, 0): (3, 0),
    (2, 1): (5, 3),
    (2, 2): (6, 3),
    (2, 3): (1, 1),
    (3, 0): (4, 0),
    (3, 1): (5, 0),
    (3, 2): (2, 2),
    (3, 3): (1, 0),
    (4, 0): (6, 1),
    (4, 1): (5, 1),
    (4, 2): (3, 2),
    (4, 3): (1, 3),
    (5, 0): (6, 0),
    (5, 1): (2, 3),
    (5, 2): (3, 3),
    (5, 3): (4, 3),
    (6, 0): (1, 2),
    (6, 1): (2, 0),
    (6, 2): (5, 2),
    (6, 3): (4, 2),
}
#  12
#  3
# 45
# 6
N = 50
face_locations = [
    [None, 1, 2],
    [None, 3, None],
    [4, 5, None],
    [6, None, None],
]
# (face, direction) -> (face_direction)
transitions = {
    (1, 0): (2, 0),
    (1, 1): (3, 1),
    (1, 2): (4, 0),
    (1, 3): (6, 0),
    (2, 0): (5, 2),
    (2, 1): (3, 2),
    (2, 2): (1, 2),
    (2, 3): (6, 3),
    (3, 0): (2, 3),
    (3, 1): (5, 1),
    (3, 2): (4, 1),
    (3, 3): (1, 3),
    (4, 0): (5, 0),
    (4, 1): (6, 1),
    (4, 2): (1, 0),
    (4, 3): (3, 0),
    (5, 0): (2, 2),
    (5, 1): (6, 2),
    (5, 2): (4, 2),
    (5, 3): (3, 3),
    (6, 0): (5, 3),
    (6, 1): (2, 1),
    (6, 2): (1, 1),
    (6, 3): (4, 3),
}


def extract(xmin, xmax, ymin, ymax, grid):
    result = []
    for x in range(xmin, xmax):
        result.append(grid[x][ymin:ymax])
    return result


def parse_input2(path: str):
    p = Path(path)
    content, instructions = p.read_text().split("\n\n")
    content = re.sub(r"\n$", "", content).split("\n")

    faces = [[] for _ in range(6)]
    for i, row in enumerate(face_locations):
        for j, face in enumerate(row):
            if face is None:
                continue
            faces[face - 1] = extract(i * N, (i + 1) * N, j * N, (j + 1) * N, content)

    return faces, parse_instructions(instructions)


def get_coord(direction, offset):
    """
    get the x,y coordinates when arriving on a face in a certain direction
    offset is the distance to the edge on the left orthogonally from the direction
    """
    match direction:
        case 0:
            return offset, 0
        case 1:
            return 0, N - 1 - offset
        case 2:
            return N - 1 - offset, N - 1
        case 3:
            return N - 1, offset


def get_face_coord(faces, current_face):
    for i, row in enumerate(face_locations):
        for j, face in enumerate(row):
            if face == current_face:
                return i, j


def get_original_coord(faces, current_face, x, y):
    i, j = get_face_coord(faces, current_face)
    return i * N + x, j * N + y


def main2(faces, instructions):
    x, y = 0, 0
    current_face = 1
    current_dir = 0

    for direction in instructions:
        if isinstance(direction, int):
            new_x = x
            new_y = y
            for i in range(direction):
                new_face = current_face
                new_dir = current_dir
                match current_dir:
                    case 0:
                        new_y += 1
                        if new_y == N:
                            new_face, new_dir = transitions[(current_face, current_dir)]
                            new_x, new_y = get_coord(new_dir, new_x)
                    case 2:
                        new_y -= 1
                        if new_y == -1:
                            new_face, new_dir = transitions[(current_face, current_dir)]
                            new_x, new_y = get_coord(new_dir, N - 1 - new_x)
                    case 1:
                        new_x += 1
                        if new_x == N:
                            new_face, new_dir = transitions[(current_face, current_dir)]
                            new_x, new_y = get_coord(new_dir, N - 1 - new_y)
                    case 3:
                        new_x -= 1
                        if new_x == -1:
                            new_face, new_dir = transitions[(current_face, current_dir)]
                            new_x, new_y = get_coord(new_dir, new_y)
                if faces[new_face - 1][new_x][new_y] == "#":
                    break
                current_face = new_face
                current_dir = new_dir
                x, y = new_x, new_y
        else:
            current_dir = get_next_dir(current_dir, direction)
    x, y = get_original_coord(faces, current_face, x, y)
    return 1000 * (x + 1) + 4 * (y + 1) + current_dir


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    if second_part:
        print(f"result: {main2(*parse_input2(input_filepath))}", file=sys.stdout)
    else:
        print(f"result: {main1(*parse_input1(input_filepath))}", file=sys.stdout)
