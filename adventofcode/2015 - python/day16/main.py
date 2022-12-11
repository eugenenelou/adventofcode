import sys

ticker_tape = dict(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1,
)


def parse_input(input):
    sues = []
    for raw_sue in input:
        sue = {}
        sues.append(sue)
        for clue in raw_sue.rstrip().split(": ", maxsplit=1)[1].split(", "):
            k, v = clue.split(": ")
            sue[k] = int(v)
    return sues


def specific_match(k, v):
    match k:
        case "cats" | "tree":
            return ticker_tape[k] < v
        case "pomeranians" | "goldfish":
            return ticker_tape[k] > v
    return ticker_tape[k] == v


def match1(sue):
    return all(ticker_tape[k] == v for k, v in sue.items())


def match2(sue):
    return all(specific_match(k, v) for k, v in sue.items())


def main1(input):
    sues = parse_input(input)
    matching_sues = []
    for i, sue in enumerate(sues):
        if match1(sue):
            matching_sues.append(i + 1)
    return matching_sues


def main2(input):
    sues = parse_input(input)
    matching_sues = []
    for i, sue in enumerate(sues):
        if match2(sue):
            matching_sues.append(i + 1)
    return matching_sues


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
