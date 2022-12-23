import sys
from collections import defaultdict
from pathlib import Path

directions_to_check = [
    [(-1, 0), (-1, 1), (-1, -1)],  # N, NE, NW
    [(1, 0), (1, 1), (1, -1)],  # S, SE, SW
    [(0, -1), (-1, -1), (1, -1)],  # W, NW, SW
    [(0, 1), (-1, 1), (1, 1)],  # E, NE, SE
]


def parse_input():
    input_filepath = sys.argv[1]
    p = Path(input_filepath)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    elves = set()
    for i, line in enumerate(content.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                elves.add((i, j))
    return elves


def translate(point, translation):
    return point[0] + translation[0], point[1] + translation[1]


def display(elves):
    minx = min(x for x, _ in elves)
    miny = min(y for _, y in elves)
    maxx = max(x for x, _ in elves)
    maxy = max(y for _, y in elves)

    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            print("#" if (x, y) in elves else ".", end="")
        print("")


def main1():
    elves = parse_input()
    print("Start")
    display(elves)
    for i in range(10):
        # first half
        targets = defaultdict(list)
        for elf in elves:
            proposed = False
            if any(
                translate(elf, translation) in elves
                for directions in directions_to_check
                for translation in directions
            ):
                for j in range(4):
                    directions = directions_to_check[(j + i) % 4]
                    if all(
                        translate(elf, translation) not in elves
                        for translation in directions
                    ):
                        targets[translate(elf, directions[0])].append(elf)
                        proposed = True
                        break
            if not proposed:
                targets[elf].append(elf)
        # second half
        new_elves = set()
        for target, proposing_elves in targets.items():
            match proposing_elves:
                case [elf]:
                    new_elves.add(target)
                case many_elves:
                    new_elves.update(many_elves)
        elves = new_elves

    print("\nEnd")
    display(elves)

    minx = min(x for x, _ in elves)
    miny = min(y for _, y in elves)
    maxx = max(x for x, _ in elves)
    maxy = max(y for _, y in elves)

    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves)


def main2():
    elves = parse_input()
    print("Start")
    display(elves)
    i = 0
    while True:
        # first half
        targets = defaultdict(list)
        for elf in elves:
            proposed = False
            if any(
                translate(elf, translation) in elves
                for directions in directions_to_check
                for translation in directions
            ):
                for j in range(4):
                    directions = directions_to_check[(j + i) % 4]
                    if all(
                        translate(elf, translation) not in elves
                        for translation in directions
                    ):
                        targets[translate(elf, directions[0])].append(elf)
                        proposed = True
                        break
            if not proposed:
                targets[elf].append(elf)
        # second half
        new_elves = set()
        for target, proposing_elves in targets.items():
            match proposing_elves:
                case [elf]:
                    new_elves.add(target)
                case many_elves:
                    new_elves.update(many_elves)
        if sorted(elves) == sorted(new_elves):
            print("\nEnd")
            display(new_elves)
            return i + 1
        elves = new_elves
        i += 1


if __name__ == "__main__":
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    print(f"result: {main2() if second_part else main1()}", file=sys.stdout)
