import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    mapping = {}
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
        lr = lrs[i % len(lrs)]
        i += 1
        key = mapping[key][0 if lr == "L" else 1]
    return i


# see 2016 day 15
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def solve_diophantine(a: int, b: int, c: int) -> tuple[int, int]:
    gcd, x1, y1 = extended_gcd(a, b)
    if c % gcd != 0:
        raise Exception(f"gcd={gcd} is not a multiple of c={c}")
    x = x1 * c // gcd
    y = y1 * (c // gcd)
    return x, y


def merge_equations(p1, c1, p2, c2) -> tuple[int, int]:
    gcd, _, _ = extended_gcd(p1, p2)
    x0, _ = solve_diophantine(p1, p2, c2 - c1)
    p3 = p1 * p2 // gcd
    c3 = c1 + p1 * x0
    c3 = (p3 + c3 % p3) % p3  # simplify c3 to be in [0, p3[
    return p3, c3


def solve_multi_diophantine(*equations: tuple[int, int]) -> tuple[int, int]:
    """
    from a list of (a, b) solve for all b[i]x+a[i] equals
    """
    (p1, c1), (p2, c2), *rest = equations
    p3, c3 = merge_equations(p1, c1, p2, c2)
    if not rest:
        return p3, c3
    return solve_multi_diophantine((p3, c3), *equations[2:])


def main2(input_):
    lrs, mapping = input_
    keys = [key for key in mapping if key.endswith("A")]

    def get_cycle_equation(key) -> tuple[int, int]:
        i = 0
        found_ends = {}
        while True:
            lr = lrs[i % len(lrs)]
            i += 1
            key = mapping[key][0 if lr == "L" else 1]
            if key.endswith("Z"):
                if last_z := (found_ends.get(key)):
                    return i - last_z, last_z  # (cycle, offset)
                found_ends[key] = i

    equations = [get_cycle_equation(key) for key in keys]
    return solve_multi_diophantine(*equations)[0]


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
