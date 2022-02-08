import sys
from itertools import permutations


def main(input):
    edges = {}
    nodes = set()
    for edge in input:
        node1, _, node2, _, distance = edge.rstrip().split(" ")
        edges[(node1, node2)] = edges[(node2, node1)] = int(distance)
        nodes.add(node1)
        nodes.add(node2)

    def cost(p):
        p = list(p)
        return sum(edges[(n1, n2)] for n1, n2 in zip(p[:-1], p[1:]))

    result = max(cost(p) for p in permutations(nodes))
    return result


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
