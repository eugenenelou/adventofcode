import sys
from collections import Counter
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for row in content.split("\n"):
        hand, bet = row.split()
        #
        res.append((hand, int(bet)))
    return res


HANDS: dict[tuple, int] = {
    (5,): 7,
    (1, 4): 6,
    (2, 3): 5,
    (1, 1, 3): 4,
    (1, 2, 2): 3,
    (1, 1, 1, 2): 2,
    (1, 1, 1, 1, 1): 1,
}


def main1(input_):
    return sum(
        (rank + 1) * bet
        for rank, (_, bet) in enumerate(
            sorted(
                (
                    (
                        HANDS[tuple(sorted(Counter(hand).values()))],
                        hand.replace("A", "Z").replace("T", "B").replace("K", "Y"),
                    ),
                    bet,
                )
                for hand, bet in input_
            )
        )
    )


def get_hand_value(hand):
    counter = Counter(hand)
    jokers = counter.pop("J", 0)
    values = sorted(counter.values())
    if values:
        values[-1] += jokers
    else:
        values = [jokers]
    return tuple(values)


def main2(input_):
    return sum(
        (rank + 1) * bet
        for rank, (_, bet) in enumerate(
            sorted(
                (
                    (
                        HANDS[get_hand_value(hand)],
                        hand.replace("A", "Z")
                        .replace("T", "B")
                        .replace("K", "Y")
                        .replace("J", "1"),
                    ),
                    bet,
                )
                for hand, bet in input_
            )
        )
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
