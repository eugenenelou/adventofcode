import sys
from itertools import permutations


def happiness(scores, people):
    def score(perm):
        return scores[(perm[-1], perm[0])] + sum(
            scores[(p1, p2)] for p1, p2 in zip(perm[:-1], perm[1:])
        )

    return max(score(perm) + score(list(reversed(perm))) for perm in permutations(people))


def parse_input(input):
    scores = {}
    people = set()
    for instruction in input:
        p1, _, gain_or_lose, n, _, _, _, _, _, _, p2 = instruction.rstrip()[:-1].split(" ")
        scores[(p1, p2)] = int(n) if gain_or_lose == "gain" else -int(n)
        people.add(p1)
        people.add(p2)
    return scores, people


def main1(input):
    return happiness(*parse_input(input))


def main2(input):
    scores, people = parse_input(input)
    people.add("me")
    for person in people:
        scores[("me", person)] = 0
        scores[(person, "me")] = 0
    return happiness(scores, people)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
