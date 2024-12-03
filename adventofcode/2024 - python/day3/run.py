import sys
from pathlib import Path
import re


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content


REGEX = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def main1(input_):
    return sum(
        int(match.group(1)) * int(match.group(2)) for match in REGEX.finditer(input_)
    )


def main2(input_):
    return sum(main1(parts.split("don't()")[0]) for parts in input_.split("do()"))


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
