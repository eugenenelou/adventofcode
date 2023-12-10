import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


mappings: dict[tuple[int, int, str], tuple[int, int]] = {
    (-1, 0, "F"): (0, 1),
    (0, -1, "F"): (1, 0),
    (1, 0, "L"): (0, 1),
    (0, -1, "L"): (-1, 0),
    (1, 0, "J"): (0, -1),
    (0, 1, "J"): (-1, 0),
    (-1, 0, "7"): (0, -1),
    (0, 1, "7"): (1, 0),
    (1, 0, "L"): (0, 1),
    (0, -1, "L"): (-1, 0),
    (-1, 0, "|"): (-1, 0),
    (1, 0, "|"): (1, 0),
    (0, -1, "-"): (0, -1),
    (0, 1, "-"): (0, 1),
}


def main1(input_):
    start = x_start, y_start = next(
        (x, y)
        for x, row in enumerate(input_)
        for y, char in enumerate(row)
        if char == "S"
    )

    def get_coord(x, y):
        if x < 0 or y < 0 or x >= len(input_) or y >= len(input_[0]):
            return "."
        return input_[x][y]

    starting_dirs = [
        (x, y)
        for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if (x, y, get_coord(x_start + x, y_start + y)) in mappings
    ]
    if len(starting_dirs) != 2:
        raise Exception("We assume there are exactly 2 starting directions")

    direction = starting_dirs[0]
    current = start
    i = 0
    while True:
        i += 1
        new_current = (current[0] + direction[0], current[1] + direction[1])
        value = get_coord(*new_current)
        if value == "S":
            return (i + 1) // 2
        direction = mappings[
            (
                direction[0],
                direction[1],
                value,
            )
        ]
        current = new_current


def main2(input_):
    """
    When iterating each row, count the number of times we went through the loop
    if we went through an odd number of times, we are in the loop and should count
    the tiles not part of the loop
    """
    start = x_start, y_start = next(
        (x, y)
        for x, row in enumerate(input_)
        for y, char in enumerate(row)
        if char == "S"
    )

    def get_coord(x, y):
        if x < 0 or y < 0 or x >= len(input_) or y >= len(input_[0]):
            return "."
        return input_[x][y]

    print("start", x_start, y_start)
    starting_dirs = [
        (x, y)
        for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if (x, y, get_coord(x_start + x, y_start + y)) in mappings
    ]
    if len(starting_dirs) != 2:
        raise Exception("We assume there are exactly 2 starting directions")

    direction = starting_dirs[0]
    current = start
    i = 0
    loop_points = {start}
    while True:
        i += 1
        new_current = (current[0] + direction[0], current[1] + direction[1])
        value = get_coord(*new_current)
        if value == "S":
            break
        direction = mappings[
            (
                direction[0],
                direction[1],
                value,
            )
        ]
        current = new_current
        loop_points.add(current)

    # Replace S by it's actual character
    s_replace = next(
        char
        for (x1, y1, char), (x2, y2) in mappings.items()
        if (-x1, -y1) in starting_dirs and (x2, y2) in starting_dirs
    )
    input_ = [row.replace("S", s_replace) for row in input_]
    count = 0

    # whether a transition counts as going through a loop tile
    in_loop_transition = {
        ("up", "-"): False,
        ("down", "-"): False,
        ("up", "|"): True,
        ("down", "|"): True,
        ("up", "F"): False,
        ("down", "F"): False,
        ("up", "L"): False,
        ("down", "L"): False,
        ("up", "J"): True,
        ("down", "J"): False,
        ("up", "7"): False,
        ("down", "7"): True,
    }

    for x, row in enumerate(input_):
        in_the_loop = False
        up_down = "up"  # doesn't matter
        for y, value in enumerate(row):
            # When encountering an F or L we can "go around" the loop
            # if we are coming from the correct side
            # eg: ...F--7... does not go through the loop
            # but ...F--J... does
            if value == "F":
                up_down = "up"
            elif value == "L":
                up_down = "down"
            if (x, y) in loop_points:
                if in_loop_transition[(up_down, value)]:
                    in_the_loop = not in_the_loop
                print(value, end="")
            elif in_the_loop:
                count += 1
                print("I", end="")
            else:
                print(".", end="")
        print("")
    return count


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
