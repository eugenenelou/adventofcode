import sys
from collections import defaultdict
from functools import cache
from itertools import chain
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    edges = defaultdict(list)
    for line in content.split("\n"):
        a, b = line.split("-")
        edges[a].append(b)
        edges[b].append(a)
    return edges


def get_triplets(neighbors, edges, n, has_t=None):
    @cache
    def check_connections(nodes, node, depth, has_t: bool):
        if depth == 1:
            if has_t:
                yield tuple(sorted(chain(nodes, [node])))
            return
        for neighbor in neighbors[node]:
            if neighbor not in nodes and all(
                (neighbor, previous_node) in edges for previous_node in nodes
            ):
                yield from check_connections(
                    tuple(sorted(chain(nodes, [node]))),
                    neighbor,
                    depth - 1,
                    has_t or neighbor.startswith("t"),
                )

    seen_triplets = set()
    for node in neighbors:
        for triplet in check_connections(
            (), node, n, has_t=node.startswith("t") if has_t is None else has_t
        ):
            if triplet not in seen_triplets:
                yield triplet
                seen_triplets.add(triplet)


def main1(neighbors):
    edges = {(a, b) for a, bs in neighbors.items() for b in bs}
    return len(set(get_triplets(neighbors, edges, n=3)))


def main2(neighbors):
    n = 3
    edges = {(a, b) for a, bs in neighbors.items() for b in bs}
    while True:
        n += 1
        print("n", n)
        triplet_iter = iter(get_triplets(neighbors, edges, n=n, has_t=True))
        solution = next(triplet_iter)
        try:
            next(triplet_iter)
        except StopIteration:
            print(f"found solution for {n=}")
            return ",".join(solution)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
