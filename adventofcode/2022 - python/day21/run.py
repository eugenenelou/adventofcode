import sys
from functools import lru_cache
from pathlib import Path


def parse_input(path: str, second_part=False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    monkeys = {}
    for line in content.split("\n"):
        monkey, job = line.split(": ")
        try:
            n = int(job)
            monkeys[monkey] = n
        except ValueError:
            monkeys[monkey] = job.split(" ")
    return monkeys


def main1(monkeys):
    @lru_cache
    def get_monkey(name):
        match monkeys[name]:

            case int(a):
                return a
            case (m1, "*", m2):
                return get_monkey(m1) * get_monkey(m2)
            case (m1, "+", m2):
                return get_monkey(m1) + get_monkey(m2)
            case (m1, "-", m2):
                return get_monkey(m1) - get_monkey(m2)
            case (m1, "/", m2):
                return get_monkey(m1) // get_monkey(m2)
            case x:
                raise Exception(f"not understood: {x}")

    return get_monkey("root")


class HumanException(Exception):
    pass


def main2(monkeys):
    @lru_cache
    def get_monkey(name):
        if name == "humn":
            raise HumanException
        match monkeys[name]:

            case int(a):
                return a
            case (m1, "*", m2):
                return get_monkey(m1) * get_monkey(m2)
            case (m1, "+", m2):
                return get_monkey(m1) + get_monkey(m2)
            case (m1, "-", m2):
                return get_monkey(m1) - get_monkey(m2)
            case (m1, "/", m2):
                return get_monkey(m1) // get_monkey(m2)
            case x:
                raise Exception(f"not understood: {x}")

    a, _, b = monkeys["root"]
    try:
        target, other = get_monkey(a), b
    except HumanException:
        target, other = get_monkey(b), a

    while other != "humn":
        a, op, b = monkeys[other]
        try:
            n, other = get_monkey(a), b
            match op:
                case "+":
                    target -= n
                case "-":
                    target = n - target
                case "*":
                    target = target // n
                case "/":
                    target = n // target
        except HumanException:
            n, other = get_monkey(b), a
            match op:
                case "+":
                    target -= n
                case "-":
                    target += n
                case "*":
                    target = target // n
                case "/":
                    target *= n
    return target


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath, second_part=second_part)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
