from functools import cache
import sys
from pathlib import Path
from typing import Never
from utils.parser import IterableParser

type Data = tuple[str, str]

class GroupParser:
    def parse(self, input_: str, *, context: None):
        a, b = input_.split('-')
        if len(b) > len(a) +1:
            raise ValueError("More than one level of order of magnitude to handle")
        return a,b

parser = IterableParser[Data, None](GroupParser(), separator=",")

def sum_to_n(n: int)->int:
    return n * (n+1) // 2

def handle_pair(data: Data):
    a, b = data
    if len(b)  % 2 == 0:
        half_b = int(b[:len(b)//2])
        if int(f"{half_b}{half_b}")>int(b):
            half_b -=1
    else:
        half_b = 10**(len(b)//2) - 1
    if len(a) % 2 == 0:
        half_a = int(a[:len(a)//2])
        if int(f"{half_a}{half_a}")<int(a):
            half_a+=1
    else:
        half_a = 10**(len(a)//2)
    if half_a > half_b:
        return 0
    res = (sum_to_n(half_b) - sum_to_n(half_a - 1)) * (10**len(str(half_b)) + 1)
    print(f"{a=}, {half_a=}, {b=}, {half_b=}, {res=}")
    return res

def main1(data: list[Data]):
    return sum(handle_pair(pair) for pair in data)


@cache
def get_multiplicator(part_len: int, m: int):
    res = 1
    for i in range(1,m):
        res += 10**(part_len*i)
    return res

def get_from_part(n: int, m: int):
    multiplicator = get_multiplicator(len(str(n)), m)
    return n * multiplicator


def test(n,m, r):
    assert get_from_part(n, m) == r, f"{get_from_part(n, m)} != {r}"

test(12, 3, 121212)

multiples_to_check = [2, 3, 5, 7] # only need to check primes

def handle_pair2(data: Data):
    a, b = data
    a_n ,b_n = int(a), int(b)
    res=0
    seen = set()
    for m in multiples_to_check:
        if len(a) % m == 0:
            part_len = len(a) // m
            i = int(a[:part_len])
            maxi = min(b_n, 10**(len(a))-1)
        elif len(b) % m == 0:
            part_len = len(b) // m
            i = 10**(part_len-1)
            maxi = b_n
        else:
            continue
        n = get_from_part(i, m)
        while n <= maxi:
            if n >= a_n and n not in seen:
                seen.add(n)
                res += n

            i += 1
            n = get_from_part(i, m)
    return res

def main2(data: list[Data]):
    return sum(handle_pair2(pair) for pair in data)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parser.parse(Path(input_filepath).read_text())
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
