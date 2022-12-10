import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        if line == "noop":
            yield line, None
        else:
            a, b = line.split(" ")
            yield a, int(b)


def main1(input_):
    result = 0
    t = 0
    registry = 1

    def count_results():
        nonlocal result
        if t % 40 == 20:
            result += t * registry

    for instruction, value in input_:
        if instruction == "noop":
            t += 1
            count_results()
        else:
            t += 1
            count_results()
            t += 1
            count_results()
            registry += value
    return result


def main2(input_):
    t = 0
    registry = 1

    def draw():
        print("#" if abs(registry - ((t - 1) % 40)) <= 1 else ".", end="")
        if t % 40 == 0:
            print("")

    for instruction, value in input_:
        if instruction == "noop":
            t += 1
            draw()
        else:
            t += 1
            draw()
            t += 1
            draw()
            registry += value


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
