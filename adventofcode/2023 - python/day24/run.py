import re
import sys
from dataclasses import dataclass, replace
from math import gcd, inf, sqrt
from pathlib import Path


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @property
    def line_coefs(self) -> tuple[float, float]:
        a = self.dy / self.dx
        return a, self.y - a * self.x

    def intersection(self, other: "Hailstone") -> None | tuple[float, float]:
        a, b = self.line_coefs
        # print("a", a, b)
        c, d = other.line_coefs
        # print("c", c, d)
        if a == c:
            return None
        x = (d - b) / (a - c)
        return x, a * x + b

    def is_ahead(self, x: float, y: float) -> bool:
        return (x - self.x) * self.dx > 0

    def get_t(self, t):
        return self.x + t * self.dx, self.y + t * self.dy, self.z + t * self.dz


MIN = 7
MAX = 27
MIN = 200000000000000
MAX = 400000000000000


def out_of_bound(x: float, y: float) -> bool:
    return x < MIN or x > MAX or y < MIN or y > MAX


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        coords, speeds = row.split(" @ ")
        x, y, z = map(int, re.split(r",[^\d-]+", coords))
        dx, dy, dz = map(int, re.split(r",[^\d-]+", speeds))
        res.append(Hailstone(x, y, z, dx, dy, dz))
    return res


def main1(input_):
    count = 0
    for i, hailstone1 in enumerate(input_):
        for hailstone2 in input_[i + 1 :]:
            intersection = hailstone1.intersection(hailstone2)
            if intersection is None:
                continue
            x, y = intersection
            if (
                out_of_bound(x, y)
                or not hailstone1.is_ahead(x, y)
                or not hailstone2.is_ahead(x, y)
            ):
                continue
            count += 1
    return count


def cross_product(v1, v2):
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )


def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


def vec_sub(v1, v2):
    return v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]


def check_collision(x1, y1, z1, dx1, dy1, dz1, x2, y2, z2, dx2, dy2, dz2) -> bool:
    return (
        dot_product(
            cross_product((dx1, dy1, dz1), (dx2, dy2, dz2)),
            vec_sub((x2, y2, z2), (x1, y1, z1)),
        )
        == 0
    )


def vec_norm(v):
    return sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def distance_line(h1, h2) -> float:
    n = cross_product((h1.dx, h1.dy, h1.dz), (h2.dx, h2.dy, h2.dz))
    return dot_product(
        n,
        vec_sub((h2.x, h2.y, h2.z), (h1.x, h1.y, h1.z)),
    ) / vec_norm(n)


def get_intersection(h1, h2):
    n = cross_product((h1.dx, h1.dy, h1.dz), (h2.dx, h2.dy, h2.dz))
    t1 = dot_product(
        cross_product((h2.dx, h2.dy, h2.dz), n),
        vec_sub((h1.x, h1.y, h1.z), (h2.x, h2.y, h2.z)),
    ) / dot_product(n, n)
    return h1.get_t(t1)


def main2(input_):
    maxi = 400
    # assume the speed of the stone is small enough
    # change the referential so that the stone does not move and testing
    # all the small speed vectors
    # if all the stones collide at the same place (the condition tested
    # is just that they collide, it's enough) then it's the correct speed vector
    # and the initial stone position is at the intersection of all hailstones
    for dx in range(-maxi, maxi):
        for dy in range(-maxi, maxi):
            for dz in range(-maxi, maxi):
                ok = True
                for h1, h2 in zip(input_[:-1], input_[1:]):
                    if not check_collision(
                        h1.x,
                        h1.y,
                        h1.z,
                        h1.dx - dx,
                        h1.dy - dy,
                        h1.dz - dz,
                        h2.x,
                        h2.y,
                        h2.z,
                        h2.dx - dx,
                        h2.dy - dy,
                        h2.dz - dz,
                    ):
                        ok = False
                        break
                if ok:
                    h1 = input_[0]
                    h2 = input_[1]
                    return get_intersection(
                        replace(h1, dx=h1.dx - dx, dy=h1.dy - dy, dz=h1.dz - dz),
                        replace(h2, dx=h2.dx - dx, dy=h2.dy - dy, dz=h2.dz - dz),
                    )
    raise Exception("not found")


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
