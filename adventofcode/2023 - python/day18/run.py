import sys
from bisect import insort
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from operator import attrgetter
from pathlib import Path


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


DIR_BY_CHAR = {
    "U": Direction.UP,
    "R": Direction.RIGHT,
    "D": Direction.DOWN,
    "L": Direction.LEFT,
}

DIR_VECTORS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        direction, distance, color = row.split()
        res.append((DIR_BY_CHAR[direction], int(distance), color[2:-1]))
    return res


def main1(input_):
    x_values = [0]
    y_values = [0]
    for direction, distance, _ in input_:
        match direction:
            case Direction.UP:
                y_values.append(y_values[-1] - distance)
            case Direction.DOWN:
                y_values.append(y_values[-1] + distance)
            case Direction.LEFT:
                x_values.append(x_values[-1] - distance)
            case Direction.RIGHT:
                x_values.append(x_values[-1] + distance)
    height = max(x_values) - min(x_values) + 1
    width = max(y_values) - min(y_values) + 1
    x_offset = min(x_values)
    y_offset = min(y_values)

    print("height", height)
    print("width", width)
    print("x_offset", x_offset)
    print("y_offset", y_offset)
    grid = [[None] * width for _ in range(height)]

    going_rights: set[tuple[int, int]] = set()
    going_lefts: set[tuple[int, int]] = set()

    x = -x_offset
    y = -y_offset
    grid[x][y] = input_[0][0]
    count = 0
    # make the perimeter
    last_direction: Direction | None = None
    for direction, distance, _ in input_:
        # print("direction", direction, distance)
        if last_direction is None:
            pass
        elif (last_direction.value + 1) % 4 == direction.value:
            going_rights.add((x, y))
        elif (last_direction.value + 3) % 4 == direction.value:
            going_lefts.add((x, y))
        last_direction = direction
        vector = DIR_VECTORS[direction]
        for i in range(distance):
            x += vector[0]
            y += vector[1]
            if i == distance - 1:
                grid[x][y] = direction
            else:
                grid[x][y] = "|" if direction in (Direction.UP, Direction.DOWN) else "-"
            count += 1

    for y in range(width):
        for x in range(height):
            print("#" if grid[x][y] else ".", end="")
        print("")

    grid2 = deepcopy(grid)

    for x, row in enumerate(grid):
        is_inside = False
        for y, direction in enumerate(row):
            if direction is None:  # not on the perimeter
                if is_inside:
                    count += 1
            else:
                if is_inside and (x, y) in going_rights:
                    is_inside = False
                elif not is_inside and (x, y) in going_lefts:
                    is_inside = True
                elif direction == "-":
                    is_inside = not is_inside
            if is_inside:
                grid2[x][y] = True

    print("")
    for y in range(width):
        for x in range(height):
            print("#" if grid2[x][y] else ".", end="")
        print("")

    return count


def parse_input2(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        _, _, color = row.split()
        distance = int(color[2:-2], 16)
        direction = Direction(int(color[-2]))
        res.append((direction, distance))
    return res


@dataclass(frozen=True, slots=True)
class Segment:
    start: int
    end: int  # inclusive
    x: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1

    def intersect(self, other: "Segment") -> "Segment | None":
        if self.end < other.start or other.end < self.start:
            return None
        res = self.__class__(
            max(self.start, other.start), min(self.end, other.end), self.x
        )
        return res

    def difference(self, other: "Segment") -> Iterable["Segment"]:
        if self.end < other.start or other.end < self.start:
            return [self]
        if self.start < other.start:
            res = [self.__class__(self.start, other.start - 1, self.x)]
        else:
            res = []
        if other.end < self.end:
            res.append(self.__class__(other.end + 1, self.end, self.x))
        return res


def segment_with_x_key(v: tuple[Segment, int]):
    return (v[0].x, v[0].start)


segment_key = attrgetter("x", "start")


def is_turning_right(direction: Direction, next_direction: Direction):
    return next_direction.value - direction.value in (1, -3)


def angle_on_the_inside(
    direction: Direction, next_direction: Direction, inside_on_the_right: bool
):
    """
    The angle is on the inside if turning right and the inside is on the left
    and vice versa
    """
    turning_right = is_turning_right(direction, next_direction)
    if inside_on_the_right:
        return not turning_right
    return turning_right


def main2(input_):
    inside_on_the_right = (
        sum(is_turning_right(d1, d2) for (d1, _), (d2, _) in zip(input_, input_[1:]))
        > len(input_) // 2
    )
    x, y = 0, 0
    # vertical segments of the perimeter as seen from the outside.
    # corners on the inside are not included in the segments
    vertical_segments = []
    for (last_direction, _), (direction, distance), (next_direction, _) in zip(
        chain(input_[-1:], input_[:-1]), input_, chain(input_[1:], input_[:1])
    ):
        match direction:
            case Direction.UP:
                new_y = y - distance
                new_x = x
                vertical_segments.append(
                    Segment(
                        new_y
                        + angle_on_the_inside(
                            Direction.UP, next_direction, inside_on_the_right
                        ),
                        y
                        - angle_on_the_inside(
                            last_direction, Direction.UP, inside_on_the_right
                        ),
                        x,
                    )
                )
            case Direction.DOWN:
                new_y = y + distance
                new_x = x
                vertical_segments.append(
                    Segment(
                        y
                        + angle_on_the_inside(
                            last_direction, Direction.DOWN, inside_on_the_right
                        ),
                        new_y
                        - (
                            angle_on_the_inside(
                                Direction.DOWN, next_direction, inside_on_the_right
                            )
                        ),
                        x,
                    )
                )
            case Direction.LEFT:
                new_x = x - distance
                new_y = y
            case Direction.RIGHT:
                new_x = x + distance
                new_y = y
            case _:
                raise ValueError
        x = new_x
        y = new_y
    y_min, y_max = min(seg.start for seg in vertical_segments), max(
        seg.end for seg in vertical_segments
    )
    x_min = min(seg.x for seg in vertical_segments)

    vertical_segments.sort(key=segment_key)

    # segments, starting on the outside and compared to the perimeter vertical segments
    # increasing the total area if inside the perimeter
    accumulated_segments = [(Segment(y_min, y_max, x_min - 1), False)]
    count = 0
    while accumulated_segments:
        first_segment, is_inside = accumulated_segments.pop(0)
        for i, vertical_segment in enumerate(vertical_segments):
            if (inter_segment := vertical_segment.intersect(first_segment)) is not None:
                if is_inside:
                    count += inter_segment.length * (
                        vertical_segment.x - first_segment.x + 1
                    )

                insort(
                    accumulated_segments,
                    (inter_segment, not is_inside),
                    key=segment_with_x_key,
                )

                vertical_segments.pop(i)

                for rest_segment in first_segment.difference(vertical_segment):
                    insort(
                        accumulated_segments,
                        (rest_segment, is_inside),
                        key=segment_with_x_key,
                    )
                for rest_segment in vertical_segment.difference(first_segment):
                    insort(vertical_segments, rest_segment, key=segment_key)
                break

    return count


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = (parse_input2 if second_part else parse_input)(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
