from collections import Counter
from curses import raw
from dataclasses import dataclass
from functools import cache
from itertools import combinations, permutations
from multiprocessing import Value
from operator import itemgetter
import sys
from pathlib import Path
import sys

def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_start_values, raw_operations = content.split("\n\n")
    start_values = {}
    for line in raw_start_values.split("\n"):
        key, value = line.split(": ")
        start_values[key] = bool(int(value))

    operations = {}
    for line in raw_operations.split('\n'):
        raw, result = line.split(" -> ")
        operations[result] = raw.split(' ')
    return start_values, operations


def get_int(prefix: str, keys, get_value):
    znames = sorted((key for key in keys if key.startswith(prefix)), reverse=True)
    # print('znames', znames)
    zvalues = [str(int(get_value(name))) for name in znames]
    # print('zvalues', zvalues)
    return int("".join(zvalues), 2)

def main1(input_):
    start_values, operations = input_

    @cache
    def get_value(name):
        if (value:= start_values.get(name)) is not None:
            return value
        a, op, b = operations[name]

        va = get_value(a)
        vb = get_value(b)
        match op:
            case 'AND':
                return va and vb
            case 'OR':
                return va or vb
            case 'XOR':
                return va ^ vb

    return get_int("z", operations, get_value)

N_PAIRS = 2

sys.setrecursionlimit(100)

def main2(input_):
    start_values, operations = input_

    @cache
    def get_value(name):
        if (value:= start_values.get(name)) is not None:
            return value
        a, op, b = operations[name]

        va = get_value(a)
        vb = get_value(b)
        match op:
            case 'AND':
                return va and vb
            case 'OR':
                return va or vb
            case 'XOR':
                return va ^ vb

    x = get_int("x", start_values, lambda x: start_values[x])
    y = get_int("y", start_values, lambda y: start_values[y])

    def swap(eight_keys, operations):
        for i in range(0, N_PAIRS*2, 2):
            a, b = eight_keys[i], eight_keys[i+1]
            operations[a], operations[b] = operations[b], operations[a]

    def get_identifier(eight_keys):
        return tuple(sorted(tuple(sorted([eight_keys[i], eight_keys[i+1]]))for i in range(0, N_PAIRS*2, 2)))

    print('x', x)
    print('y', y)
    target = x + y


    res = get_int("z", operations, get_value)
    print('target ^ res', target ^ res, format(target^res, 'b'))
    i = 0

    def get_all_keys(key):
        if key in start_values:
            # yield key
            pass
        else:
            a, _, b = operations[key]
            yield key
            yield from get_all_keys(a)
            yield from get_all_keys(b)
        
    all_keys = []
    for idx, bit in enumerate(reversed(format(target^res, 'b'))):
        if bit == "1":
            print('idx', idx)
            keys = sorted(set(get_all_keys(f"z{idx:02d}")))
            print('get_all_keys', keys)
            all_keys.extend(keys)
    counter = Counter(all_keys)
    print('counter', counter)

    def check_xy(key):
        if key in operations:
            keyA, _, keyB = operations[key]

            ax, ay = check_xy(keyA)
            bx, by = check_xy(keyB)
            return [*ax, *bx], [*ay ,*by]
        return [key] if key.startswith("x") else [], [key] if key.startswith("y") else []

    for key in sorted(operations.keys()):
        if key.startswith("z"):
            idx = int(key[1:])
            has_x, has_y = check_xy(key)

            if idx == 0:
                print('has_x', has_x)
                print('has_y', has_y)
            xs = set(has_x)
            ys = set(has_y)
            # print('\nkey', key)
            # print('has_x', has_x, 'has_y', has_y)

            for i in range(idx-1, idx +1):
                if f"x{i:02d}" not in xs:
                    print(f'missing x{i:02d} for {idx=}')
            for i in range(idx-1, idx +1):
                if f"y{i:02d}" not in ys:
                    print(f'missing y{i:02d} for {idx=}')
    # for eight_keys in combinations(operations.keys(), N_PAIRS*2):
    #     i+=1
    #     if i % 1000 == 0:
    #         print('i', i)
    #     eight_keys = list(eight_keys)
    #     seen_perms = set()
    #     for eight_keys_permutations in permutations(eight_keys):
    #         get_value.cache_clear()
    #         id_ = get_identifier(eight_keys_permutations)
    #         eight_keys_permutations = list(eight_keys_permutations)
    #         # print('id_', id_)
    #         if id_ in seen_perms:
    #             continue
    #         # print('id_', id_)
    #         seen_perms.add(id_)
    #         swap(eight_keys_permutations, operations)

    #         # if id_ == (("z00", "z05"), ('z01', "z02")):
    #         #     print(id_)
    #         #     print(operations)

    #         try:
    #             z = get_int("z", operations, get_value)
    #             if z == target:
    #                 return ",".join(sorted(eight_keys))
    #         except RecursionError:
    #             pass
    #         swap(eight_keys_permutations, operations)

    raise ValueError("Not found")

if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
