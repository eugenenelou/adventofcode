import sys
from functools import cache
from pathlib import Path
from pprint import pprint


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_patterns, goals = content.split("\n\n")
    pattern_list = raw_patterns.split(", ")
    targets = goals.split("\n")

    pattern_tree = {}
    for pattern in pattern_list:
        tree = pattern_tree
        for char in pattern:
            tree = tree.setdefault(char, {})
        tree[""] = True

    return pattern_list, pattern_tree, targets


def check_feasible(target_idx, target, tree, full_tree):
    if tree.get("") is True:
        if target_idx == len(target) or check_feasible(
            target_idx, target, full_tree, full_tree
        ):
            return True
    elif target_idx == len(target):
        return False
    subtree = tree.get(target[target_idx])
    return subtree is not None and check_feasible(
        target_idx + 1, target, subtree, full_tree
    )


def main1(input_):
    pattern_list, pattern_tree, targets = input_
    res = 0
    for i, target in enumerate(targets):
        print("i", i)
        res += bool(check_feasible(0, target, pattern_tree, pattern_tree))
    return res


def main2(input_):
    pattern_list, full_tree, targets = input_

    @cache
    def check_feasible_2(target_idx, target, key):
        res = 0

        def get(key, tree):
            if not key:
                return tree
            return get(key[1:], tree[key[0]])

        tree = get(key, full_tree)

        if tree.get("") is True:
            if target_idx == len(target):
                return 1
            res += check_feasible_2(target_idx, target, ())
        elif target_idx == len(target):
            return 0
        subtree = tree.get(target[target_idx])
        if subtree is not None:
            res += check_feasible_2(target_idx + 1, target, (*key, target[target_idx]))
        return res

    return sum(check_feasible_2(0, target, ()) for target in targets)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
