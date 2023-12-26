import sys
from bisect import insort, insort_left
from collections import defaultdict, deque
from operator import attrgetter, itemgetter
from pathlib import Path
from random import shuffle


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    transitions = defaultdict(set)
    nodes = set()
    for row in content.split("\n"):
        from_node, to_nodes = row.split(": ")
        nodes.add(from_node)
        for to_node in to_nodes.split(" "):
            nodes.add(to_node)
            transitions[from_node].add(to_node)
            transitions[to_node].add(from_node)
    return transitions, list(nodes)


def main1(input_):
    transitions, nodes = input_
    while True:
        result = find_split(transitions, nodes)
        if result is not None:
            return result
        print("invalid result, trying again")
        shuffle(nodes)


def find_split(transitions: dict[str, set[str]], names: list[str]) -> int | None:
    group_left = set(names[: len(names) // 2])
    balance_ordered = []
    balance_by_name = {}
    # order by biggest imbalance of mixed vs left or right
    ordering = lambda x: x[3] - (x[2] + x[4])
    for name in names:
        left = 0
        mixed = 0
        right = 0
        is_left = name in group_left
        for to in transitions[name]:
            match (is_left, to in group_left):
                case (True, True):
                    left += 1
                case (True, False) | (False, True):
                    mixed += 1
                case (False, False):
                    right += 1
        balance = [name, is_left, left, mixed, right]
        insort(balance_ordered, balance, key=ordering)
        balance_by_name[name] = balance
    total_mixed = sum(item[3] for item in balance_ordered)
    i = 0
    while total_mixed > 6:
        i += 1
        if i > 2000:  # arbitrary value, it works in 1000-1500 steps usually
            return None
        name, is_left, left, mixed, right = item = balance_ordered.pop()
        item[1] = is_left = not is_left
        if is_left:
            item[2] = mixed
            item[3] = right
            item[4] = 0
            total_mixed += right - mixed
        else:
            item[2] = 0
            item[3] = left
            item[4] = mixed
            total_mixed += left - mixed
        # don't reinsert it at the end to avoid loop
        insort_left(balance_ordered, item, key=ordering)
        for to in transitions[name]:
            _, item_is_left, item_left, item_mixed, item_right = item = balance_by_name[
                to
            ]
            match is_left, item_is_left:
                case (True, True):
                    item[2] += 1
                    item[3] -= 1
                    total_mixed -= 1
                case (True, False):
                    item[3] += 1
                    item[4] -= 1
                    total_mixed += 1
                case (False, True):
                    item[2] -= 1
                    item[3] += 1
                    total_mixed += 1
                case (False, False):
                    item[3] -= 1
                    item[4] += 1
                    total_mixed -= 1
        balance_ordered.sort(key=ordering)
    left, right = 0, 0
    for _, is_left, _, _, _ in balance_ordered:
        if is_left:
            left += 1
        else:
            right += 1
    if left == 0 or right == 0:
        # invalid result where all nodes are in the same group
        return None
    return left * right


def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
