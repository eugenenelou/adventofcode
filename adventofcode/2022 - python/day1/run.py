import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    return content.split("\n")


def main1(input):
    current_elf = 0
    max_elf = 0
    for c in input:
        if c == "":
            max_elf = max(current_elf, max_elf)
            current_elf = 0
        else:
            current_elf += int(c)
    return max_elf


def main2(input):
    current_elf = 0
    top_three_elves = [0, 0, 0]
    for c in input:
        if c == "":
            top_three_elves = sorted(top_three_elves + [current_elf])[1:]
            current_elf = 0
        else:
            current_elf += int(c)
    return sum(top_three_elves)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input)}", file=sys.stdout)
    else:
        print(f"result: {main1(input)}", file=sys.stdout)
