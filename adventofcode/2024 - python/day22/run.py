import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return list(map(int, content.split("\n")))


MODULO = 16777216


def get_next_secret(a: int):
    b = ((a * 64) ^ a) % MODULO
    c = ((b // 32) ^ b) % MODULO
    d = ((c * 2048) ^ c) % MODULO
    return d


def get_many_next(a: int, n: int):
    for _ in range(n):
        a = get_next_secret(a)
    return a


def main1(input_):
    return sum(get_many_next(a, 2000) for a in input_)


def main2(input_):
    sellers = [{} for _ in range(len(input_))]
    for i, (start, seller) in zip(input_, sellers, strict=True):
        start_n_bananas = start % 10
        deltas = [None]
        last_value = get_next_secret(start)
        last_n_bananas = last_value % 10
        deltas.append(last_n_bananas - start_n_bananas)

        for _ in range(2):
            value = get_next_secret(last_value)
            n_bananas = value % 10
            deltas.append(n_bananas - last_n_bananas)
            last_value = value
            last_n_bananas = n_bananas

        for _ in range(1997):
            value = get_next_secret(last_value)
            n_bananas = value % 10
            deltas.append(n_bananas - last_n_bananas)
            deltas.pop(0)
            last_value = value
            last_n_bananas = n_bananas

            seller.setdefault(tuple(deltas), n_bananas)

    all_keys = set()
    all_keys.update(*(seller.keys() for seller in sellers))
    return max(sum(seller.get(deltas, 0) for seller in sellers) for deltas in all_keys)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
