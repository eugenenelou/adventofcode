from collections.abc import Iterator
from dataclasses import dataclass
import sys
from pathlib import Path
import re


@dataclass
class Problem:
    ax: int
    ay: int
    bx: int
    by: int
    target_x: int
    target_y: int


def extract_two_ints(line: str) -> Iterator[int]:
    for match in re.finditer(r"\d+", line):
        yield int(match.group(0))


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    problems = []
    for raw_problem in content.split("\n\n"):
        first, second, third = raw_problem.split("\n")
        problems.append(
            Problem(
                *extract_two_ints(first),
                *extract_two_ints(second),
                *extract_two_ints(third),
            )
        )
    return problems


def solve(problem, delta: int):
    problem.target_x += delta
    problem.target_y += delta
    b = (problem.ay * problem.target_x - problem.target_y * problem.ax) / (
        problem.ay * problem.bx - problem.by * problem.ax
    )
    a = (problem.target_x - problem.bx * b) / problem.ax
    return a, b


def main(problems, delta=0):
    res = 0
    for problem in problems:
        a, b = solve(problem, delta)
        if a.is_integer() and b.is_integer():
            res += int(3 * a + b)
    return res


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main(input_, delta=10000000000000)}", file=sys.stdout)
    else:
        print(f"result: {main(input_)}", file=sys.stdout)
