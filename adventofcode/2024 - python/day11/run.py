from functools import cache
import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [int(x) for x in content.split()]


# def main(stones, n: int):
#     for _ in range(n):
#         new_stones = []
#         for stone in stones:
#             if stone == 0:
#                 new_stones.append(1)
#             elif (l := len(str(stone))) % 2 == 0:
#                 half = l // 2
#                 x = 10**half
#                 new_stones.append(stone // x)
#                 new_stones.append(stone % x)
#             else:
#                 new_stones.append(stone * 2024)

#         stones = new_stones

#     return len(stones)


def main(stones, n):
    @cache
    def get(stone, n) -> int:
        new_stones = []
        if n == 0:
            return 1
        if stone == 0:
            new_stones.append(1)
        elif (l := len(str(stone))) % 2 == 0:
            half = l // 2
            x = 10**half
            new_stones.append(stone // x)
            new_stones.append(stone % x)
        else:
            new_stones.append(stone * 2024)

        return sum(get(stone, n - 1) for stone in new_stones)

    return sum(get(stone, n) for stone in stones)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2
    input_ = parse_input(input_filepath)
    print(f"result: {main(input_, n=int(sys.argv[2]))}", file=sys.stdout)
