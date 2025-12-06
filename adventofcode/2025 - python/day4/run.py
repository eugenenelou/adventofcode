import sys
from pathlib import Path
from utils.parser import IterableParser, FnParser

type Data = list[bool]


parser = IterableParser[Data, None](FnParser(lambda x: [c == '@' for c in x]))

def read(x: int, y: int, grid: list[list[bool]]):
    if x < 0 or y < 0:
        return False
    try:
        return grid[x][y]
    except IndexError:
        return False

def main1(data: list[Data]):
    res = 0
    for x, row in enumerate(data):
        for y, cell in enumerate(row):
            n = sum(read(x+dx, y+dy, data) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            if cell and n <= 4: # accept equal because the current cell is counted
                res += 1
    return res


def main2(data: list[Data]):
    res = 0
    found = True
    while found:
        found = False
        for x, row in enumerate(data):
            for y, cell in enumerate(row):
                n = sum(read(x+dx, y+dy, data) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                if cell and n <= 4: # accept equal because the current cell is counted
                    res += 1
                    data[x][y] = False
                    found = True
    return res



if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
