import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path


class BrickIdGenerator:
    def __init__(self):
        self.next_id = 0

    def __call__(self):
        id_ = self.next_id
        self.next_id += 1
        return id_


@dataclass(slots=True)
class Brick:
    id: int
    x: int
    dx: int
    y: int
    dy: int
    z: int
    dz: int


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    bricks = []
    id_generator = BrickIdGenerator()
    for row in content.split("\n"):
        row_coord_a, row_coord_b = row.split("~")
        xa, ya, za = map(int, row_coord_a.split(","))
        xb, yb, zb = map(int, row_coord_b.split(","))
        bricks.append(
            Brick(
                id=id_generator(),
                x=min(xa, xb),
                y=min(ya, yb),
                z=min(za, zb),
                dx=abs(xa - xb) + 1,
                dy=abs(ya - yb) + 1,
                dz=abs(za - zb) + 1,
            )
        )
    return bricks


def compute_supports(bricks: list[Brick]):
    xmax = max(b.x + b.dx for b in bricks)
    ymax = max(b.y + b.dy for b in bricks)
    zmax = max(b.z + b.dz for b in bricks)

    # (z, x, y)
    # + 1 for z so the plan above is always defined
    volume: list[list[list[int | None]]] = [
        [[None for _ in range(ymax)] for _ in range(xmax)] for _ in range(zmax + 1)
    ]

    def set_brick_coord(brick, x, y, z):
        for dz in range(brick.dz):
            for dx in range(brick.dx):
                for dy in range(brick.dy):
                    volume[brick.z + dz][brick.x + dx][brick.y + dy] = None
                    volume[z + dz][x + dx][y + dy] = brick.id
        brick.x = x
        brick.y = y
        brick.z = z

    for brick in bricks:
        set_brick_coord(brick, brick.x, brick.y, brick.z)

    bricks.sort(key=attrgetter("z"))

    # let the bricks fall
    for brick in bricks:
        z = None
        for new_z in range(brick.z - 1, 0, -1):
            plan = volume[new_z]
            if all(
                plan[brick.x + dx][brick.y + dy] is None
                for dx in range(brick.dx)
                for dy in range(brick.dy)
            ):
                z = new_z
            else:
                break
        if z is not None:
            set_brick_coord(brick, brick.x, brick.y, z)
    supported_by = defaultdict(set)
    supporting = defaultdict(set)
    for brick in bricks:
        plan_above = volume[brick.z + brick.dz]
        supporting_ids = {
            brick_id
            for dx in range(brick.dx)
            for dy in range(brick.dy)
            if (brick_id := plan_above[brick.x + dx][brick.y + dy]) is not None
        }
        for brick_id in supporting_ids:
            supported_by[brick_id].add(brick.id)
            supporting[brick.id].add(brick_id)

    return supported_by, supporting


def main1(bricks: list[Brick]):
    supported_by, supporting = compute_supports(bricks)
    res = 0
    for brick in bricks:
        if not supporting[brick.id] or all(
            len(supported_by[supported_id]) > 1 for supported_id in supporting[brick.id]
        ):
            res += 1
    return res


def main2(bricks: list[Brick]):
    supported_by, supporting = compute_supports(bricks)
    res = 0
    for brick in bricks:
        fallen_bricks = {brick.id}
        falling_bricks = deque()
        falling_bricks.append(brick.id)
        count = 0
        while falling_bricks:
            falling_brick = falling_bricks.popleft()
            for potential_brick in supporting[falling_brick]:
                if potential_brick in fallen_bricks:
                    continue
                if all(
                    supporting_brick in fallen_bricks
                    for supporting_brick in supported_by[potential_brick]
                ):
                    fallen_bricks.add(potential_brick)
                    falling_bricks.append(potential_brick)
                    count += 1
        res += count
    return res


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
