import sys
from bisect import insort_left
from collections import defaultdict
from enum import Enum
from functools import cache
from operator import itemgetter
from pathlib import Path
from typing import Iterator


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


DIR_VECTORS = {
    Direction.UP: (-1, 0),
    Direction.LEFT: (0, -1),
    Direction.DOWN: (1, 0),
    Direction.RIGHT: (0, 1),
}


def multiply_vector(vector: tuple[int, int], n: int) -> tuple[int, int]:
    return vector[0] * n, vector[1] * n


Delta = tuple[Direction, int]
Node = tuple[int, int]
NodeWithCost = tuple[Node, int]


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [[int(char) for char in row] for row in content.split("\n")]


@cache
def get_new_deltas(
    direction: Direction, mini=1, maxi=3
) -> list[tuple[tuple[int, int], Delta]]:
    new_direction = Direction((direction.value + 1) % 4)
    dir_vector = DIR_VECTORS[new_direction]
    res = []
    for i in range(mini - 1, maxi):
        res.append((multiply_vector(dir_vector, i + 1), (new_direction, i + 1)))

    new_direction = Direction((direction.value + 3) % 4)
    dir_vector = DIR_VECTORS[new_direction]
    for i in range(mini - 1, maxi):
        res.append((multiply_vector(dir_vector, i + 1), (new_direction, i + 1)))
    return res


def get_neighbours(
    node: Node, direction_from: Direction, mini: int, maxi: int
) -> Iterator[tuple[Node, Delta]]:
    x, y = node
    for (dx, dy), delta in get_new_deltas(direction_from, mini, maxi):
        yield (x + dx, y + dy), delta


chars = {
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.RIGHT: ">",
    Direction.UP: "^",
}

get_cost_from_tuple = itemgetter(1)


def get_unit_vector(x: int, y: int) -> tuple[int, int]:
    if x == 0:
        return (0, 1) if y > 0 else (0, -1)
    return (1, 0) if x > 0 else (-1, 0)


def main1(input_, mini=1, maxi=3):
    height, width = len(input_), len(input_[0])

    for row in input_:
        print("".join(map(str, row)))

    def is_out_of_bound(node: Node) -> bool:
        return node[0] < 0 or node[1] < 0 or node[0] >= height or node[1] >= width

    goal = (height - 1, width - 1)
    reached_nodes = defaultdict(dict)
    reached_nodes[(0, 0)] = {Direction.UP: 0, Direction.LEFT: 0}
    # from_nodes is for displaying the path
    from_nodes = defaultdict(list)

    nodes = [((0, 0), 0, Direction.RIGHT), ((0, 0), 0, Direction.DOWN)]

    def get_cost(from_node: Node, to_node: Node) -> int:
        dx, dy = get_unit_vector(from_node[0] - to_node[0], from_node[1] - to_node[1])
        x, y = to_node
        cost = 0
        while (x, y) != from_node:
            cost += input_[x][y]
            x += dx
            y += dy
        return cost

    while nodes:
        node, cost, direction_from = nodes.pop(0)

        if node == goal:
            node = goal
            last_direction = None
            while node != (0, 0):
                if last_direction is None:
                    possible_directions = (Direction.RIGHT, Direction.DOWN)
                else:
                    possible_directions = (
                        Direction((last_direction.value + 1) % 4),
                        Direction((last_direction.value + 3) % 4),
                    )
                from_node, last_direction = next(
                    (node, direction)
                    for node, direction in from_nodes[node]
                    if direction in possible_directions
                )
                dx, dy = get_unit_vector(from_node[0] - node[0], from_node[1] - node[1])
                x, y = node
                while (x, y) != from_node:
                    char = chars[last_direction]
                    input_[x][y] = char
                    x += dx
                    y += dy

                node = from_node

            print("")
            for x in range(height):
                for y in range(width):
                    print(input_[x][y], end="")
                print("")

            return cost

        for neighbour, (direction, n) in get_neighbours(
            node, direction_from, mini, maxi
        ):
            if is_out_of_bound(neighbour):
                continue
            from_directions = reached_nodes[neighbour]
            if (current_n := from_directions.get(direction)) is None:
                from_directions[direction] = n
                from_nodes[neighbour].append((node, direction))
            elif current_n <= n:  # equal should not happen
                continue
            else:
                from_directions.pop(direction)
                from_directions[direction] = n
            x, y = neighbour
            insort_left(
                nodes,
                (neighbour, cost + get_cost(node, neighbour), direction),
                key=get_cost_from_tuple,
            )
    raise Exception(f"Could not reach {goal=}")


def main2(input_):
    return main1(input_, mini=4, maxi=10)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
