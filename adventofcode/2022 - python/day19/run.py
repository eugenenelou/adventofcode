import re
import sys
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable
import time
from math import prod

robot_type_regex = re.compile(r"Each ([a-z]+)")
cost_regex = re.compile(r"(\d+) (obsidian|clay|ore)")


@dataclass
class RobotTemplate:
    type: str
    cost: dict[str, int]

    @classmethod
    def from_string(cls, string) -> "RobotTemplate":
        type_match = robot_type_regex.search(string)
        cost = {}
        for match in re.finditer(cost_regex, string):
            cost[match.group(2)] = int(match.group(1))
        return cls(type=type_match.group(1), cost=cost)


@dataclass
class Blueprint:
    robot_templates: list[RobotTemplate]

    @classmethod
    def from_string(cls, string) -> "Blueprint":
        return cls(
            robot_templates=[
                RobotTemplate.from_string(raw_robot)
                for raw_robot in string.split(":")[-1].split(".")
                if raw_robot
            ]
        )


@dataclass(slots=True, frozen=True)
class Situation:
    max_time: int
    t: int
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    n_ore_robot: int = 0
    n_clay_robot: int = 0
    n_obsidian_robot: int = 0
    n_geode_robot: int = 0

    def tick(self, robot_template: RobotTemplate = None):
        kwargs = dict(
            t=self.t + 1,
            ore=self.ore + self.n_ore_robot,
            clay=self.clay + self.n_clay_robot,
            obsidian=self.obsidian + self.n_obsidian_robot,
            geode=self.geode + self.n_geode_robot,
        )
        if robot_template:
            attr_name = f"n_{robot_template.type}_robot"
            kwargs[attr_name] = getattr(self, attr_name) + 1
            for resource, cost in robot_template.cost.items():
                kwargs[resource] -= cost
        return replace(self, **kwargs)

    def affordable_robots(self, blueprint: Blueprint) -> Iterable[str]:
        for robot_template in blueprint.robot_templates:
            if all(
                getattr(self, resource) >= cost for resource, cost in robot_template.cost.items()
            ):
                yield robot_template

    @property
    def id(self):
        """
        for this given identifier, the optimal solution
        for the remaining time remains the same
        """
        return (
            self.t,
            self.ore,
            self.clay,
            self.obsidian,
            self.n_ore_robot,
            self.n_clay_robot,
            self.n_obsidian_robot,
        )

    @property
    def min_possible_geodes(self):
        return self.geode + (self.max_time - self.t) * self.n_geode_robot

    @property
    def max_possible_geodes(self):
        # In case we succeed in creating one geode robot every minute
        n = self.max_time - self.t - 1
        return self.min_possible_geodes + n * (n + 1) // 2


def max_geodes(blueprint: Blueprint, max_time: int) -> int:
    robots = defaultdict(int)
    robots["ore"] = 1
    situations = {Situation(max_time=max_time, t=0, n_ore_robot=1)}
    for t in range(max_time):
        print(
            "t",
            t,
            "n_situations",
            len(situations),
            "max_geodes: ",
            max(s.geode for s in situations),
        )
        next_situations = defaultdict(set)
        for situation in situations:
            affordable_count = 0
            for robot_type in situation.affordable_robots(blueprint):
                next_situation = situation.tick(robot_type)
                next_situations[next_situation.id].add(next_situation)
                affordable_count += 1
            if affordable_count < 4:
                next_situation = situation.tick()
                # we shouldn't skip buying a robot if we can afford any of them
                next_situations[next_situation.id].add(next_situation)
        situations = set()
        for possible_next_situations in next_situations.values():
            situations.add(max(possible_next_situations, key=lambda s: s.min_possible_geodes))

        min_max = max(s.min_possible_geodes for s in situations)
        situations = [s for s in situations if s.max_possible_geodes >= min_max]
    res = max(situations, key=lambda s: s.geode)
    print("res: ", res.geode, res)
    return res.geode


def parse_input(path: str, second_part=False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [Blueprint.from_string(line) for line in content.split("\n")]


def main1(blueprints):
    # this takes almost 28min
    return sum(
        (i + 1) * max_geodes(blueprint, max_time=24) for i, blueprint in enumerate(blueprints)
    )


def main2(blueprints):
    # this takes 66min
    results = [max_geodes(blueprint, max_time=32) for blueprint in blueprints[:3]]
    print("results", results)
    return prod(results)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath, second_part=second_part))
    start_time = time.time()
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
    end_time = time.time()
    print(f"It took {end_time - start_time:02f}s")
