import sys
from pathlib import Path
import re

input_regex = re.compile(r"[^\d-]+(-?\d+)[^\d-]+(-?\d+)[^\d-]+(-?\d+)[^\d-]+(-?\d+)")


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        match = input_regex.match(line)
        yield (int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4)))


def manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def main1(input_):
    visited = set()
    for i, (sensor, beacon) in enumerate(input_):
        print(f"{i:02d}/{len(input_)}")
        dist = manhattan(sensor, beacon)
        for i in range(-dist, dist + 1):
            dist_i = abs(i)
            for j in range(dist_i - dist, dist - dist_i + 1):
                visited.add((sensor[0] + i, sensor[1] + j))
    for sensor, beacon in input_:
        visited.remove((sensor[0], sensor[1]))
        try:
            visited.remove((beacon[0], beacon[1]))
        except KeyError:
            pass  # the same beacon for different sensors
    # # return sum(1 for x, y in visited if y == 10)
    # l10 = [x for x, y in visited if y == 10]
    # print(sorted(l10), len(l10))
    return len(visited)


def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
