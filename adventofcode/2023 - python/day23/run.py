import sys
from bisect import insort
from collections import defaultdict, deque
from enum import Enum, auto
from functools import cache
from pathlib import Path


class Tile(Enum):
    EMPTY = auto()
    WALL = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


DIRECTION_TILES = {Tile.UP, Tile.RIGHT, Tile.DOWN, Tile.LEFT}

TILE_BY_CHAR = {
    ".": Tile.EMPTY,
    "#": Tile.WALL,
    "^": Tile.UP,
    ">": Tile.RIGHT,
    "v": Tile.DOWN,
    "<": Tile.LEFT,
}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    grid = []
    for row in content.split("\n"):
        grid.append([TILE_BY_CHAR[char] for char in row])
    start = (0, next(y for y, char in enumerate(grid[0]) if char == Tile.EMPTY))
    end = (
        len(grid) - 1,
        next(y for y, char in enumerate(grid[-1]) if char == Tile.EMPTY),
    )
    return grid, start, end


# possible direction, and the Tile it's incompatible with
incompatible_dxs = {
    (0, 1): Tile.LEFT,
    (1, 0): Tile.UP,
    (0, -1): Tile.RIGHT,
    (-1, 0): Tile.DOWN,
}
possible_dxs = list(incompatible_dxs.keys())
direction_dx = {
    Tile.UP: (-1, 0),
    Tile.RIGHT: (0, 1),
    Tile.DOWN: (1, 0),
    Tile.LEFT: (1, -1),
}

Point = tuple[int, int]
Edge = tuple[Point, Point]


def insort_tuple(t: tuple[Point, ...], value: Point) -> tuple[Point, ...]:
    mutable = list(t)
    insort(mutable, value)
    return tuple(mutable)


def main1(input_):
    grid, start, end = input_
    height, width = len(grid), len(grid[0])

    # construct the graph
    nodes: set[Point] = set()
    edges: dict[tuple[Point, Point], int] = {}
    from_nodes: dict[Point, set[Point]] = defaultdict(set)
    coords = deque()
    coords.append((start, 0, (0, 0), start, True))
    i = 0

    def in_bounds(x, y):
        return x >= 0 and y >= 0 and x < height and y < width

    while coords:
        i += 1
        # print("coords", [c for c, *_ in coords])
        coord, steps, last_coord, from_coord, can_go_backward = coords.popleft()
        cx, cy = coord
        tile = grid[cx][cy]

        is_node = (
            coord == start
            or coord == end
            or sum(
                1
                for dx, dy in possible_dxs
                if in_bounds(x := cx + dx, y := cy + dy) and grid[x][y] != Tile.WALL
            )
            > 2
        )
        if is_node:
            if steps > 0:
                edges[(from_coord, coord)] = steps
                from_nodes[coord].add(from_coord)
                if can_go_backward:
                    edges[(coord, from_coord)] = steps
                    from_nodes[from_coord].add(coord)
            from_coord = coord
            steps = 0
            # assume no slope is a node
            assert tile == Tile.EMPTY, (coord, tile)
            can_go_backward = True

            if coord in nodes:
                continue
            nodes.add(coord)

        if tile in DIRECTION_TILES:
            dxs = [direction_dx[tile]]
            if not is_node:
                can_go_backward = False
        else:
            dxs = possible_dxs
        for dx, dy in dxs:
            x, y = cx + dx, cy + dy
            if (
                (x, y) == last_coord
                or not in_bounds(x, y)
                or incompatible_dxs[(dx, dy)] == (tile := grid[x][y])
                or tile == Tile.WALL
            ):
                continue
            coords.append(((x, y), steps + 1, coord, from_coord, can_go_backward))

    @cache
    def longest_path_to(node: Point, seen_nodes: tuple[Point]):
        if node == start:
            return 0
        if not (from_nodes_ := from_nodes[node]):
            raise ValueError
        values = []
        for from_node in from_nodes_:
            if from_node not in seen_nodes:
                try:
                    values.append(
                        edges[(from_node, node)]
                        + longest_path_to(from_node, insort_tuple(seen_nodes, node))
                    )
                except ValueError:
                    pass
        if len(values) != 0:
            return max(values)
        raise ValueError

    return longest_path_to(end, tuple())


def main2(input_):
    return main1(input_)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    if second_part:
        TILE_BY_CHAR["^"] = Tile.EMPTY
        TILE_BY_CHAR[">"] = Tile.EMPTY
        TILE_BY_CHAR["v"] = Tile.EMPTY
        TILE_BY_CHAR["<"] = Tile.EMPTY
        sys.setrecursionlimit(10_000)
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
