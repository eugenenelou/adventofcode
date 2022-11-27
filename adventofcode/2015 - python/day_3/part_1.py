import sys


def main(input):
    loc = (0, 0)
    visited_locs = {loc}
    for c in next(iter(input)):
        match c:
            case ">":
                loc = (loc[0] + 1, loc[1])
            case "^":
                loc = (loc[0], loc[1] + 1)
            case "<":
                loc = (loc[0] - 1, loc[1])
            case "v":
                loc = (loc[0], loc[1] - 1)
        visited_locs.add(loc)
    return len(visited_locs)


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
