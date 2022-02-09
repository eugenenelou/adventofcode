import sys
import json


def main1(input):
    j = json.loads(next(iter(input)))

    def count(data):
        match data:
            case list(l):
                return sum(count(elt) for elt in l)
            case dict(d):
                return sum(count(v) for v in d.values())
            case int(i):
                return i
            case _:
                return 0

    return count(j)


def main2(input):
    j = json.loads(next(iter(input)))

    def count(data):
        match data:
            case list(l):
                return sum(count(elt) for elt in l)
            case dict(d):
                if "red" in d or "red" in d.values():
                    return 0
                return sum(count(v) for v in d.values())
            case int(i):
                return i
            case _:
                return 0

    return count(j)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
