import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        elf1, elf2 = line.split(",")
        p1, p2 = map(int, elf1.split("-"))
        p3, p4 = map(int, elf2.split("-"))
        yield sorted([(p1, p2), (p3, p4)], key=lambda x: (x[0], -x[1]))


def main1(input_):
    return sum(p1 <= p3 and p2 >= p4 for (p1, p2), (p3, p4) in input_)


def main2(input_):
    return sum(p2 >= p3 and p1 <= p4 for (p1, p2), (p3, p4) in input_)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
