import math
import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    time, distance = content.split("\n")
    return list(
        zip(
            map(int, time.split(":", maxsplit=1)[1].strip().split()),
            map(int, distance.split(":", maxsplit=1)[1].strip().split()),
        )
    )


def original_main1(input_):
    res = 1
    for i, (time, record_distance) in enumerate(input_):
        count = 0
        for j in range(time):
            speed = j
            distance = (time - j) * speed
            if distance > record_distance:
                count += 1
        res *= count
    return res


def main1(input_):
    res = 1
    for i, (time, record_distance) in enumerate(input_):
        # solving x(time-x) > record_distance
        det = time * time - 4 * record_distance
        r1 = (time + math.sqrt(det)) / 2
        r2 = (time - math.sqrt(det)) / 2
        count = math.floor(r1 - 1e-9) - math.ceil(r2 + 1e-9) + 1
        print(f"{count} number of ways for race {i}")
        res *= count
    return res


def main2(input_):
    time = int("".join(str(t) for t, _ in input_))
    distance = int("".join(str(d) for _, d in input_))
    return main1([(time, distance)])


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
