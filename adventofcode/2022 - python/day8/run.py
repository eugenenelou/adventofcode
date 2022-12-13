import sys
from functools import lru_cache
from pathlib import Path
from pprint import pprint
from tkinter import scrolledtext


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [[int(x) for x in line] for line in content.split('\n')]

def main1(grid):
    results = [[False] * len(grid[0]) for _ in range(len(grid))]
    n_rows = len(grid)
    n_cols = len(grid[0])
    for i in range(n_rows):
        # >
        last_value = -1
        row = grid[i]
        for j in range(n_cols):
            if (v := row[j]) > last_value:
                results[i][j] = True
            last_value = max(v, last_value)
        # <
        last_value = -1
        row = grid[i]
        for j in range(n_cols-1,-1,-1):
            if (v := row[j]) > last_value:
                results[i][j] = True
            last_value = max(v, last_value)
    for j in range(n_cols):
        # v
        last_value = -1
        for i in range(n_rows):
            if (v := grid[i][j]) > last_value:
                results[i][j] = True
            last_value = max(v, last_value)
        # ^
        last_value = -1
        for i in range(n_rows-1,-1,-1):
            if (v := grid[i][j]) > last_value:
                results[i][j] = True
            last_value = max(v, last_value)
    for i, row in enumerate(results):
        print(f"{i+1:02d}", "".join('X' if v else " " for v in row))
    return sum(v for row in results for v in row)

def count_trees(current_tree, trees):
    trees = list(trees)
    res = 0
    for tree in trees:
        res += 1
        if tree >= current_tree:
            break
    return res


def main2(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    res = 0
    for i in range(1, n_rows-1):
        for j in range(1, n_cols -1):
            current_tree = grid[i][j]
            print (f"i={i}, j={j}",
                count_trees(current_tree, grid[i][j+1:]),
                count_trees(current_tree, grid[i][:j][::-1]),
                count_trees(current_tree, (grid[x][j] for x in range(i-1, -1, -1))),
                count_trees(current_tree, (grid[x][j] for x in range(i+1, n_rows)))
            )
            score = (
                count_trees(current_tree, grid[i][j+1:])
                * count_trees(current_tree, grid[i][:j][::-1])
                * count_trees(current_tree, (grid[x][j] for x in range(i-1, -1, -1)))
                * count_trees(current_tree, (grid[x][j] for x in range(i+1, n_rows)))
            )
            if score > res:
                res = score
    return res



if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
