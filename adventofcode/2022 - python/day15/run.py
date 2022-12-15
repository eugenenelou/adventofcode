import sys
from pathlib import Path
import re
from dataclasses import dataclass
from itertools import chain

input_regex = re.compile(r"[^\d-]+(-?\d+)[^\d-]+(-?\d+)[^\d-]+(-?\d+)[^\d-]+(-?\d+)")


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    sensors = []
    lines = content.split("\n")
    for line in lines[1:]:
        match = input_regex.match(line)
        sensors.append(
            ((int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4))))
        )
    return sensors, int(lines[0])


def manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def main1(sensors, max_coord, y_target=2_000_000):
    visited = set()
    for i, (sensor, beacon) in enumerate(sensors):
        print(f"{i:02d}/{len(sensors)}")
        dist = manhattan(sensor, beacon)
        for i in range(-dist, dist + 1):
            dist_i = abs(i)
            if sensor[1] + dist_i - dist <= y_target <= sensor[1] + dist - dist_i:
                # for j in range(dist_i - dist, dist - dist_i + 1):
                #     visited.add((sensor[0] + i, sensor[1] + j))
                visited.add((sensor[0] + i, y_target))
    for sensor, beacon in sensors:
        try:
            visited.remove((sensor[0], sensor[1]))
        except KeyError:
            pass
        try:
            visited.remove((beacon[0], beacon[1]))
        except KeyError:
            pass  # the same beacon for different sensors
    # # return sum(1 for x, y in visited if y == 10)
    # l10 = [x for x, y in visited if y == 10]
    # print(sorted(l10), len(l10))
    return len(visited)


SIZE = 4_000_000
# SIZE = 20


@dataclass
class Area:
    top_left_limit: int = 0  # <= x + y
    top_right_limit: int = SIZE  # >= x - y
    bot_left_limit: int = -SIZE  # <= x - y
    bot_right_limit: int = 2 * SIZE  # >= x + y

    def points(self):
        """return the points of the area that fit in the total space"""
        x_min = (self.top_left_limit + self.bot_left_limit) // 2
        x_max = (self.top_right_limit + self.bot_right_limit) // 2
        for x in range(max(x_min, 0), min(SIZE, x_max) + 1):
            y_min = max(0, self.top_left_limit - x, x - self.top_right_limit)
            y_max = min(SIZE, x - self.bot_left_limit, self.bot_right_limit - x)
            for y in range(y_min, y_max + 1):
                yield (x, y)

    def __and__(self, other: "Area") -> "Area | None":
        # disjointed:
        if (
            self.top_left_limit > other.bot_right_limit
            or self.bot_left_limit > other.top_right_limit
            or self.top_right_limit < other.bot_left_limit
            or self.bot_right_limit < other.top_left_limit
        ):
            return None
        area = Area(
            top_left_limit=max(self.top_left_limit, other.top_left_limit),
            bot_left_limit=max(self.bot_left_limit, other.bot_left_limit),
            top_right_limit=min(self.top_right_limit, other.top_right_limit),
            bot_right_limit=min(self.bot_right_limit, other.bot_right_limit),
        )
        if area.out_of_bounds() or area.negative_space():
            return None
        return area

    def negative_space(self):
        return (
            self.bot_right_limit < self.top_left_limit or self.top_right_limit < self.bot_left_limit
        )

    def out_of_bounds(self):
        x_min = (self.top_left_limit + self.bot_left_limit) // 2
        x_max = (self.top_right_limit + self.bot_right_limit) // 2
        y_min = (self.top_left_limit - self.top_right_limit) // 2
        y_max = (self.bot_right_limit - self.bot_left_limit) // 2
        return x_min > SIZE or x_max < 0 or y_min > SIZE or y_max < 0

    @classmethod
    def get_half_planes(cls, center, dist):
        x, y = center
        return [
            Area(top_left_limit=x + y + dist + 1, top_right_limit=x - y + dist),
            Area(bot_right_limit=x + y - dist - 1, bot_left_limit=x - y - dist),
            Area(top_right_limit=x - y - dist - 1, bot_right_limit=x + y + dist),
            Area(bot_left_limit=x - y + dist + 1, top_left_limit=x + y - dist),
        ]


def main2(sensors, max_coord):
    # each sensors split the space into 4 half-plane of aivalable directions
    # eg:
    #   1   5
    # 1 ......
    #   ...#..
    #   ..###.
    #   ...#..
    # 5 ......
    # split the plane into:
    # x + y < 6
    # x + y > 8
    # x - y > 2
    # x - y < 0
    # we'll use rectangular areas (with a 45° angle)
    # for each sensor we'll combine the 4 constraints with the exisitng areas defined by the
    # previous constraint. Some areas will be split into 2 or 3, other will be closed.
    # in practice we'll do quarter of planes to avoid aving a lot of duplicated space between half planes
    areas = [Area()]
    n = len(sensors)
    for i, (sensor, beacon) in enumerate(sensors):
        print(f"[{i+1:02d}/{n:02d}]n areas: {len(areas)}")
        new_areas = []
        half_planes = Area.get_half_planes(center=sensor, dist=manhattan(sensor, beacon))
        for area in areas:
            for half_plane in half_planes:
                if (new_area := (area & half_plane)) is not None:
                    new_areas.append(new_area)
        areas = new_areas
    print("Final areas:")
    for a in areas:
        print(a)
    result = list(chain(*(area.points() for area in areas)))
    if len(result) != 1:
        raise Exception(f"Did not find a single point, found {len(result)}")
    x, y = result[0]
    return x * 4_000_000 + y


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(*input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(*input_)}", file=sys.stdout)
