import sys
from pathlib import Path
from utils.parser import IterableParser

type Data = ...


parser = IterableParser[Data, None](..., separator=",")

def main1(data: list[Data]):
    return 0


def main2(data: list[Data]):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
