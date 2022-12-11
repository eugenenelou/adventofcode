import sys


def new_loc(loc, direction):
    new_loc = None
    match direction:
        case ">":
            new_loc = (loc[0] + 1, loc[1])
        case "^":
            new_loc = (loc[0], loc[1] + 1)
        case "<":
            new_loc = (loc[0] - 1, loc[1])
        case "v":
            new_loc = (loc[0], loc[1] - 1)
    return new_loc


def main(input):
    loc = (0, 0)
    robot_loc = (0, 0)
    visited_locs = {loc}
    even = True
    for c in next(iter(input)):
        if even:
            loc = new_loc(loc, c)
            if not loc:
                continue
            visited_locs.add(loc)
        else:
            robot_loc = new_loc(robot_loc, c)
            if not robot_loc:
                continue
            visited_locs.add(robot_loc)
        even = not even
    return len(visited_locs)


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
