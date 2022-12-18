import sys
from pathlib import Path
from itertools import chain
from collections import defaultdict


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for line in content.split("\n"):
        x, y, z = line.split(",")
        yield int(x), int(y), int(z)


def get_lines(blocks):
    x_lines = defaultdict(set)
    y_lines = defaultdict(set)
    z_lines = defaultdict(set)
    for x, y, z in blocks:
        x_lines[(y, z)].add(x)
        y_lines[(x, z)].add(y)
        z_lines[(x, y)].add(z)

    def sort_lines(lines):
        for k, v in lines.items():
            lines[k] = sorted(v)
        return lines

    return sort_lines(x_lines), sort_lines(y_lines), sort_lines(z_lines)


def compute_surface(x_lines, y_lines, z_lines):
    result = 0
    for line in chain(x_lines.values(), y_lines.values(), z_lines.values()):
        # each consecutive block of cubes exposes 2 faces:
        l = len(line)
        if l == 1:
            result += 2
            continue
        last = line[0]
        i = 0
        while i < l - 1:
            i += 1
            if (value := line[i]) != last + 1:
                result += 2
            last = value
        result += 2
    return result


def main1(input_):
    return compute_surface(*get_lines(input_))


def get_adjacent_blocks(block):
    x, y, z = block
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def get_internal_blocks(wall_blocks, x_lines, y_lines, z_lines):
    wall_blocks = set(wall_blocks)
    x_internal_blocks = set()
    for (y, z), blocks in x_lines.items():
        for i in range(len(blocks) - 1):
            if (a := blocks[i]) + 1 < (b := blocks[i + 1]):
                for x in range(a + 1, b):
                    x_internal_blocks.add((x, y, z))

    y_internal_blocks = set()
    for (x, z), blocks in y_lines.items():
        for i in range(len(blocks) - 1):
            if (a := blocks[i]) + 1 < (b := blocks[i + 1]):
                for y in range(a + 1, b):
                    y_internal_blocks.add((x, y, z))

    z_internal_blocks = set()
    for (x, y), blocks in z_lines.items():
        for i in range(len(blocks) - 1):
            if (a := blocks[i]) + 1 < (b := blocks[i + 1]):
                for z in range(a + 1, b):
                    z_internal_blocks.add((x, y, z))

    # internal blocks that cannot reach the outside by going in a single direction
    internal_blocks = x_internal_blocks.intersection(y_internal_blocks, z_internal_blocks)

    # We now need to check if they can reach non-internal air block
    validated_internal = set()
    seen = set()
    for block in internal_blocks:
        if block in seen:
            continue
        external = False
        related_blocks = {block}
        blocks_to_check = [block]
        while blocks_to_check:
            next_blocks_to_check = set()
            for block_to_check in blocks_to_check:
                for adjacent_block in get_adjacent_blocks(block_to_check):
                    if adjacent_block in internal_blocks:
                        if adjacent_block not in related_blocks:
                            next_blocks_to_check.add(adjacent_block)
                            related_blocks.add(adjacent_block)
                    elif adjacent_block not in wall_blocks:
                        external = True
            blocks_to_check = next_blocks_to_check
        if not external:
            for b in related_blocks:
                validated_internal.add(b)
        for b in related_blocks:
            seen.add(b)
    return validated_internal


def main2(water_blocks):
    water_lines = get_lines(water_blocks)
    internal_air_blocks = get_internal_blocks(water_blocks, *water_lines)
    internal_air_lines = get_lines(internal_air_blocks)
    return compute_surface(*water_lines) - compute_surface(*internal_air_lines)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = list(parse_input(input_filepath))
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
