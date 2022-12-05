import sys
from pathlib import Path

import re

move_regex = re.compile(r"(\d+)[^\d]*(\d+)[^\d]*(\d+)")


def parse_input(path: str):
    with open(path) as f:
        content = f.readlines()

    stacks = list()
    moves = list()
    idx = None
    for i, line in enumerate(content):
        if not line.strip():
            idx = i
            break

        for j in range(0, len(line), 4):
            value = line[j + 1]
            if i == 0:
                stacks.append([value])
            else:
                stacks[j // 4].append(value)

    for line in content[idx + 1 :]:
        match = move_regex.search(line)
        moves.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))

    # clean
    stacks = [[v for v in stack[:-1][::-1] if v != " "] for stack in stacks]

    return stacks, moves


def main1(stacks, moves):
    for n, from_, to in moves:
        print("stacks", stacks)
        for _ in range(n):
            stacks[to - 1].append(stacks[from_ - 1].pop())
    return "".join([s[-1] for s in stacks])


def main2(stacks, moves):
    for n, from_, to in moves:
        print("stacks", stacks)

        stacks[to - 1].extend(stacks[from_ - 1][-n:])
        for _ in range(n):
            stacks[from_ - 1].pop()
    return "".join([s[-1] for s in stacks])


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(*input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(*input_)}", file=sys.stdout)
