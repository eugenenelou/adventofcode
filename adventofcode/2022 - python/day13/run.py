import sys
from functools import cmp_to_key
from pathlib import Path


def parse_line(line):
    i = 0
    n = len(line)
    result = []
    while i < n:
        if line[i] == "[":
            subresult, l = parse_line(line[i + 1 :])
            result.append(subresult)
            i += l + 1
        elif line[i] == "]":
            i += 1
            break
        elif line[i] == ",":
            i += 1
        else:
            j = i
            while line[j] != "," and line[j] != "]" and j < n:
                j += 1
            result.append(int(line[i:j]))
            i = j
            if line[j] == ",":
                i += 1
    return result, i


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    content = content.split("\n")
    for i in range(0, len(content), 3):
        a = parse_line(content[i][1:])[0]
        b = parse_line(content[i + 1][1:])[0]
        yield a, b

def compare_ints(a, b):
    if a < b:
        return 1
    if a > b:
        return -1
    return 0

def compare_pair(a, b) -> int:
    if not a and b:
        return 1
    if a and not b:
        return -1
    if not a and not b:
        return 0
    ha, *taila = a
    hb, *tailb = b
    match ha, hb:
        case int(), int():
            c = compare_ints(ha, hb)
        case list(la), list(lb):
            c = compare_pair(la, lb)
        case int(), list(lb):
            c = compare_pair([ha], lb)
        case list(la), int():
            c = compare_pair(la, [hb])
    if c == 1:
        return 1
    if c == -1:
        return -1
    return compare_pair(taila, tailb)

def main1(pairs):
    result = 0
    for i, (a, b) in enumerate(pairs):
        if compare_pair(a, b) == 1:
            print(f"ok for i={i+1}")
            result += i + 1
        elif compare_pair == 0:
            raise ValueError
    return result


def main2(pairs):
    lines = []
    for a, b in pairs:
        lines.append(a)
        lines.append(b)
    divider1 = [[2]]
    divider2 = [[6]]
    lines.append(divider1)
    lines.append(divider2)
    lines.sort(key=cmp_to_key(compare_pair), reverse=True)
    for i, l in enumerate(lines):
        if l == divider1:
            d1 = i+1
        if l == divider2:
            d2 = i+1
            break
    return d1*d2


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
