import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return list(map(int, content.split("\n")))


def main(input_, key, times):
    n = len(input_)
    l = [(i, number * key, (number * key) % (n - 1)) for i, number in enumerate(input_)]

    for jdx in range(times):
        for j in range(n):
            idx = next(idx for idx, data in enumerate(l) if data[0] == j)
            _, number, reduced_number = data = l[idx]
            if reduced_number == 0:
                continue
            new_idx = (idx + reduced_number) % (n - 1)
            if number > 0 and new_idx == n - 1:
                new_idx = 0
            if number < 0 and new_idx == 0:
                new_idx = n - 1
            l.pop(idx)
            l.insert(new_idx, data)

    zero_idx = next(idx for idx, data in enumerate(l) if data[1] == 0)
    print(f"{zero_idx=}")
    a, b, c = l[(zero_idx + 1000) % n][1], l[(zero_idx + 2000) % n][1], l[(zero_idx + 3000) % n][1]
    print("1000th", a)
    print("2000th", b)
    print("3000th", c)
    return a + b + c


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main(input_, key=811589153, times=10)}", file=sys.stdout)
    else:
        print(f"result: {main(input_, key=1, times=1)}", file=sys.stdout)
