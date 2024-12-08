import sys
from collections import defaultdict
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def main1(input_):
    antinodes = set()
    H = len(input_)
    W = len(input_[0])
    locations_by_antenna = defaultdict(list)

    def is_valid(x, y):
        return 0 <= x < H and 0 <= y < W

    for x, line in enumerate(input_):
        for y, char in enumerate(line):
            if char != ".":
                locations_by_antenna[char].append((x, y))

    for char, antennas in locations_by_antenna.items():
        if len(antennas) >= 2:
            for i, (x1, y1) in enumerate(antennas):
                for x2, y2 in antennas[i + 1 :]:
                    dx = x2 - x1
                    x = 2 * x1 - x2
                    y = 2 * y1 - y2
                    if is_valid(x, y):
                        antinodes.add((x, y))
                    x = 2 * x2 - x1
                    y = 2 * y2 - y1
                    if is_valid(x, y):
                        antinodes.add((x, y))
    return len(antinodes)


def main2(input_):
    antinodes = set()
    H = len(input_)
    W = len(input_[0])
    locations_by_antenna = defaultdict(list)

    def is_valid(x, y):
        return 0 <= x < H and 0 <= y < W

    for x, line in enumerate(input_):
        for y, char in enumerate(line):
            if char != ".":
                locations_by_antenna[char].append((x, y))

    for char, antennas in locations_by_antenna.items():
        if len(antennas) >= 2:
            for i, (x1, y1) in enumerate(antennas):
                for x2, y2 in antennas[i + 1 :]:
                    dx = x2 - x1
                    dy = y2 - y1

                    x = x1
                    y = y1
                    while is_valid(x, y):
                        antinodes.add((x, y))
                        x += dx
                        y += dy

                    x = x1
                    y = y1
                    while is_valid(x, y):
                        antinodes.add((x, y))
                        x -= dx
                        y -= dy
    return len(antinodes)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
