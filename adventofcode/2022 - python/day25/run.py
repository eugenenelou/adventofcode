import sys
from ast import Num
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Number:
    n: int

    @classmethod
    def from_string(cls, value):
        n = 0
        base = 1
        for char in value[::-1]:
            match char:
                case "2":
                    n += 2 * base
                case "1":
                    n += base
                case "-":
                    n -= base
                case "=":
                    n -= 2 * base
            base *= 5
        return Number(n)

    def to_string(self):
        v = []
        n = self.n
        while n:
            rest = n % 5
            n = n // 5
            match rest:
                case 0:
                    char = "0"
                case 1:
                    char = "1"
                case 2:
                    char = "2"
                case 3:
                    char = "="
                    n += 1
                case 4:
                    char = "-"
                    n += 1
            v.insert(0, char)
        return "".join(v)


def parse_input():
    input_filepath = sys.argv[1]
    p = Path(input_filepath)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    return [Number.from_string(v) for v in content.split("\n")]


def main1():
    numbers = parse_input()
    total = sum(number.n for number in numbers)
    print("total", total)
    return Number(total).to_string()


def main2():
    return 0


if __name__ == "__main__":
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    print(f"result: {main2() if second_part else main1()}", file=sys.stdout)
