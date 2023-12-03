import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


non_symbols = {*(str(i) for i in range(10)), "."}


def find_number(grid, x, y) -> tuple[int, tuple[int, int] | None]:
    if y < 0 or x < 0 or x >= len(grid) or not (char := grid[x][y]).isdigit():
        return 0, None
    y_input = y
    digits = [char]
    y = y - 1
    while y >= 0 and (char := grid[x][y]).isdigit():
        digits.insert(0, char)
        y -= 1
    y_start = y + 1
    y = y_input + 1
    grid_width = len(grid[0])
    while y < grid_width and (char := grid[x][y]).isdigit():
        digits.append(char)
        y += 1
    return int("".join(digits)), (x, y_start)


def main1(input_):
    s = 0
    seen_numbers = set()  # by coordinates of the first digit

    def add_number(number: int, start_coords):
        nonlocal s
        if start_coords is None or start_coords in seen_numbers:
            return
        seen_numbers.add(start_coords)
        s += number

    for i, row in enumerate(input_):
        for j, char in enumerate(row):
            if char not in non_symbols:
                add_number(*find_number(input_, i, j - 1))
                add_number(*find_number(input_, i, j + 1))
                if input_[i - 1][j].isdigit():
                    add_number(*find_number(input_, i - 1, j))
                else:
                    add_number(*find_number(input_, i - 1, j - 1))
                    add_number(*find_number(input_, i - 1, j + 1))
                if input_[i + 1][j].isdigit():
                    add_number(*find_number(input_, i + 1, j))
                else:
                    add_number(*find_number(input_, i + 1, j - 1))
                    add_number(*find_number(input_, i + 1, j + 1))
    return s


def main2(input_):
    s = 0
    seen_numbers = set()  # by coordinates of the first digit

    def add_number(number: int, start_coords):
        nonlocal s
        if start_coords is None or start_coords in seen_numbers:
            return None
        seen_numbers.add(start_coords)
        return number

    for i, row in enumerate(input_):
        for j, char in enumerate(row):
            if char == "*":
                numbers = []
                numbers.append(add_number(*find_number(input_, i, j - 1)))
                numbers.append(add_number(*find_number(input_, i, j + 1)))
                if input_[i - 1][j].isdigit():
                    numbers.append(add_number(*find_number(input_, i - 1, j)))
                else:
                    numbers.append(add_number(*find_number(input_, i - 1, j - 1)))
                    numbers.append(add_number(*find_number(input_, i - 1, j + 1)))
                if input_[i + 1][j].isdigit():
                    numbers.append(add_number(*find_number(input_, i + 1, j)))
                else:
                    numbers.append(add_number(*find_number(input_, i + 1, j - 1)))
                    numbers.append(add_number(*find_number(input_, i + 1, j + 1)))
                numbers = [x for x in numbers if x is not None]
                if len(numbers) == 2:
                    s += numbers[0] * numbers[1]
    return s


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
