import operator
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from pathlib import Path


@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def get_quadrant(self, H, W):
        if self.x == W // 2 or self.y == H // 2:
            return None

        return (self.x < W // 2, self.y < H // 2)


def step(robot, H, W):
    robot.x = (robot.x + robot.dx) % W
    robot.y = (robot.y + robot.dy) % H


def multiple_steps(robot, H, W, steps):
    first_pos = (robot.x, robot.y)
    pos_by_idx = {0: first_pos}
    i = 0
    while True:
        step(robot, H, W)
        i += 1
        if (robot.x, robot.y) == first_pos:
            cycle_length = i
            break
        else:
            pos_by_idx[i] = (robot.x, robot.y)
    robot.x, robot.y = pos_by_idx[(steps) % cycle_length]


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    grid, raw_robots = content.split("\n", maxsplit=1)
    W, H = map(int, grid.split(","))
    robots = []
    for line in raw_robots.split("\n"):
        robot = Robot(*map(int, re.findall(r"-?\d+", line)))
        robots.append(robot)
    return W, H, robots


def main1(input_, n=100):
    W, H, robots = input_
    quadrants = defaultdict(int)
    for robot in robots:
        multiple_steps(robot, H, W, n)
        quadrants[robot.get_quadrant(H, W)] += 1
    quadrants.pop(None, None)
    return reduce(
        operator.mul,
        quadrants.values(),
    )


def display(robots, H, W):
    g = [["."] * W for _ in range(H)]
    for robot in robots:
        g[robot.y][robot.x] = "#"
    for line in g:
        print("".join(line))


DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def count_neighbors(robots):
    places = {(robot.x, robot.y) for robot in robots}
    return sum((x + dx, y + dy) in places for x, y in places for dx, dy in DIRECTIONS)


def main2(input_):
    W, H, robots = input_
    i = 0
    while True:
        i += 1
        for robot in robots:
            step(robot, H, W)

        count = count_neighbors(robots)
        if count > 1000:
            print("i", i, "neighbours", count)
            display(robots, H, W)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
