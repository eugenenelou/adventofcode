import sys
from pathlib import Path
from enum import Enum


class Choice(Enum):
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"

    def __lt__(self, other):
        if self == Choice.ROCK:
            return other == Choice.PAPER
        if self == Choice.PAPER:
            return other == Choice.SCISSORS
        if self == Choice.SCISSORS:
            return other == Choice.ROCK

    @property
    def value(self):
        if self == Choice.ROCK:
            return 1
        if self == Choice.PAPER:
            return 2
        if self == Choice.SCISSORS:
            return 3
        raise ValueError

    def next(self, reverse=False):
        if self == Choice.ROCK:
            return Choice.SCISSORS if reverse else Choice.PAPER
        if self == Choice.PAPER:
            return Choice.ROCK if reverse else Choice.SCISSORS
        if self == Choice.SCISSORS:
            return Choice.PAPER if reverse else Choice.ROCK
        raise ValueError

    @classmethod
    def from_opponent(self, value):
        if value == "A":
            return Choice.ROCK
        if value == "B":
            return Choice.PAPER
        if value == "C":
            return Choice.SCISSORS
        raise ValueError

    @classmethod
    def from_result(cls, opponent_choice, result):
        if result == "Y":
            return opponent_choice
        if result == "X":  # loss
            return opponent_choice.next(reverse=True)
        if result == "Z":  # win
            return opponent_choice.next()
        raise ValueError


def parse_input1(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for duel in content.split("\n"):
        opponent, me = duel.split(" ")
        yield (Choice.from_opponent(opponent), Choice(me))


def parse_input2(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    for duel in content.split("\n"):
        opponent, result = duel.split(" ")
        opponent_choice = Choice.from_opponent(opponent)
        yield (opponent_choice, Choice.from_result(opponent_choice, result))


def main(input):
    result = 0
    for opponent, me in input:
        print(opponent, me, end=" ")
        round_total = 0
        # print(me, opponent, me == opponent, me > opponent)
        round_total += me.value
        if me == opponent:
            round_total += 3
        elif me > opponent:
            round_total += 6
        print("round", round_total)
        result += round_total
    return result


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    if second_part:
        print(f"result: {main(list(parse_input2(input_filepath)))}", file=sys.stdout)
    else:
        print(f"result: {main(list(parse_input1(input_filepath)))}", file=sys.stdout)
