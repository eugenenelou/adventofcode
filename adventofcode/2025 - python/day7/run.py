import sys
from pathlib import Path
from utils.parser import IterableParser, FnParser

type Data = list[bool]


parser = IterableParser[Data, None](
    IterableParser(FnParser(lambda x: x != "."), separator="")
)


def main1(data: list[Data]):
    n_split = 0
    beams = data[0].copy()
    width = len(beams)
    for line in data[1:]:
        new_beams = [False] * width
        for i, is_splitter in enumerate(line):
            if beams[i]:
                if is_splitter:
                    new_beams[i - 1] = True
                    new_beams[i + 1] = True
                    n_split += 1
                else:
                    new_beams[i] = True
        beams = new_beams
    return n_split


def main2(data: list[Data]):
    beams = [int(v) for v in data[0]]
    width = len(beams)
    for line in data[1:]:
        new_beams = [0] * width
        for i, is_splitter in enumerate(line):
            if (n := beams[i]) > 0:
                if is_splitter:
                    new_beams[i - 1] += n
                    new_beams[i + 1] += n
                else:
                    new_beams[i] += n
        beams = new_beams
    return sum(beams)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
