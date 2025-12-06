import sys
from pathlib import Path
from utils.parser import IterableParser, FnParser

type Data = list[int]


parser = IterableParser[Data, None](FnParser(lambda x: [int(c) for c in x]))

def main1(data: list[Data], n=2):
    res = 0

    for bank in data:
        s = ""
        for i in range(n, 0, -1):
            maxi = max(bank[:-i+1] if i > 1 else bank)
            idx = bank.index(maxi)
            bank = bank[idx+1:]
            s += str(maxi)
        res += int(s)

    return res


def main2(data: list[Data]):
    return main1(data, n=12)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
