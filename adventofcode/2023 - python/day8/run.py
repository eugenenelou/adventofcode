import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    mapping = {}
    print("content", content)
    lrs, _, *raw_mappings = content.split("\n")
    for raw_mapping in raw_mappings:
        key, values = raw_mapping.split(" = ")
        left, right = values[1:-1].split(", ")
        mapping[key] = (left, right)
    return lrs, mapping


def main1(input_):
    # return next(i for i, value in enumerate() if value == "ZZZ")
    lrs, mapping = input_
    key = "AAA"
    i = 0
    while key != "ZZZ":
        print("key", key)
        lr = lrs[i % len(lrs)]
        i += 1
        key = mapping[key][0 if lr == "L" else 1]
    return i


def solve_diophantine(a1, b1, a2, b2) -> tuple[int, int]:
    pass


def solve_multi_diophantine(equations: list[tuple[int, int]]):
    """
    from a list of (a, b) solve for all b[i]x+a[i] equals
    """


def main2(input_):
    lrs, mapping = input_
    i = 0
    keys = {key for key in mapping if key.endswith("A")}

    end_found_indexes = {}
    cycles_found = {}
    while any(not key.endswith("Z") for key in keys):
        lr = lrs[i % len(lrs)]
        i += 1
        keys = {mapping[key][0 if lr == "L" else 1] for key in keys}
        full_keys = [(lr, key) for key in keys]
        for full_key in full_keys:
            if full_key[1].endswith("Z"):
                if full_key in end_found_indexes and full_key not in cycles_found:
                    cycles_found[full_key] = (i, i - end_found_indexes[full_key])
                    print("cycles_found", cycles_found)
                else:
                    end_found_indexes[full_key] = i
        if all(full_key in cycles_found for full_key in full_keys):
            return solve_multi_diophantine(
                [cycles_found[full_key] for full_key in full_keys]
            )

    return i


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
