import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


DIRECTIONS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0]


def main1(input_):
    def search(x, y, dx, dy, chars):
        if len(chars) == 0:
            return True
        try:
            new_x = x + dx
            new_y = y + dy
            if new_x < 0 or new_y < 0:
                return False
            char, *rest = chars
            if input_[new_y][new_x] == char:
                return search(new_x, new_y, dx, dy, rest)
        except IndexError:
            return False
        return False

    res = 0
    for y, line in enumerate(input_):
        for x, char in enumerate(line):
            if char == "X":
                for dx, dy in DIRECTIONS:
                    if search(x, y, dx, dy, ["M", "A", "S"]):
                        res += 1
    return res


DIRECTIONS2 = [(dx, dy) for dx in (-1, 1) for dy in (-1, 1)]


def main2(input_):
    res = 0
    for y, line in enumerate(input_):
        if y == 0:
            continue
        for x, char in enumerate(line):
            if x == 0:
                continue
            if char == "A":
                try:
                    if (
                        sorted(input_[y + dy][x + dx] for dx, dy in DIRECTIONS2)
                        == ["M", "M", "S", "S"]
                        and input_[y - 1][x - 1] != input_[y + 1][x + 1]
                    ):
                        res += 1
                except IndexError:
                    pass
    return res


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
