import re
import sys
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

robot_type_regex = re.compile(r"Each ([a-z]+)")
cost_regex = re.compile(r"(\d+) (obsidian|clay|ore)")


@dataclass
class RobotTemplate:
    type: str
    cost: dict[str, int]

    @classmethod
    def from_string(cls, string) -> "RobotTemplate":
        print("parsing robot:", string)
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
    t: int
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    n_ore_robot: int = 0
    n_clay_robot: int = 0
    n_obsidian_robot: int = 0
    n_geode_robot: int = 0

    def tick(self):
        return replace(
            self,
            t=self.t + 1,
            ore=self.ore + self.n_ore_robot,
            clay=self.clay + self.n_clay_robot,
            obsidian=self.obsidian + self.n_obsidian_robot,
            geode=self.geode + self.n_geode_robot,
        )

    def add_robot(self, robot_type):
        attr_name = f"n_{robot_type}_robot"
        return replace(self, **{attr_name: getattr(self, attr_name) + 1})

    def affordable_robots(self, blueprint: Blueprint) -> Iterable[str]:
        for robot_template in blueprint.robot_templates:
            if all(
                getattr(self, resource) >= cost
                for resource, cost in robot_template.cost.items()
            ):
                yield robot_template.type

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
    def current_max_geodes(self):
        return self.geode + (MAX_TIME - self.t) * self.n_geode_robot


MAX_TIME = 24


def max_geodes(blueprint: Blueprint) -> int:
    robots = defaultdict(int)
    robots["ore"] = 1
    situations = {Situation(t=0, n_ore_robot=1)}
    for t in range(MAX_TIME):
        print("t", t, "n_situations", len(situations))
        next_situations = defaultdict(set)
        for situation in situations:
            next_situation = situation.tick()
            next_situations[next_situation.id].add(next_situation)
            for robot_type in next_situation.affordable_robots(blueprint):
                robot_situation = situation.add_robot(robot_type)
                next_situations[robot_situation.id].add(robot_situation)
        situations = set()
        for possible_next_situations in next_situations.values():
            situations.add(
                max(possible_next_situations, key=lambda s: s.current_max_geodes)
            )
    return max(situation.geode for situation in situations)


def parse_input(path: str, second_part=False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [Blueprint.from_string(line) for line in content.split("\n")]


def main1(blueprints):
    return sum(
        (i + 1) * max_geodes(blueprint) for i, blueprint in enumerate(blueprints)
    )


def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath, second_part=second_part))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
