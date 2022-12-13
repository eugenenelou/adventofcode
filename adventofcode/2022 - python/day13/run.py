import sys
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
        return -1
    if a > b:
        return 1
    return 0

def compare_lists(a, b):
    if not a and b:
        return -1
    if not a and not b:
        return 0
    if a and not b:
        return 1
    ha, *tailb = a
    hb, *tailb = b
    c = compare_pairs(ha, hb):
    

def compare_pairs(a, b):
    a_int = isinstance(a, int)
    b_int = isinstance(b, int)
    if a_int and b_int:
        return compare_ints(a ,b)
    if not a_int and not b_int:
        return compare_lists(a, b)

def main1(pairs):
    for a, b in pairs:
        


def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
