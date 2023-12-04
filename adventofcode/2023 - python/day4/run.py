import sys
from pathlib import Path


def parse_number(numbers: str) -> set[int]:
    return {int(n) for n in numbers.split()}


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    res = []
    for card in content.split("\n"):
        winning_numbers, my_numbers = card.split(": ", maxsplit=1)[1].split(" | ")
        res.append((parse_number(winning_numbers), parse_number(my_numbers)))
    return res


def main1(input_):
    s = 0
    for winning_numbers, my_numbers in input_:
        card_score = 0
        for number in my_numbers:
            if number in winning_numbers:
                card_score += 1
        if card_score > 0:
            s += 2 ** (card_score - 1)
    return s


def main2(input_):
    number_of_each_card = [1] * len(input_)

    def get_card_score(i):
        winning_numbers, my_numbers = input_[i]
        card_score = 0
        for number in my_numbers:
            if number in winning_numbers:
                card_score += 1
        return card_score

    for i in range(len(input_)):
        number_of_cards = number_of_each_card[i]
        for j in range(i + 1, i + get_card_score(i) + 1):
            number_of_each_card[j] += number_of_cards
    return sum(number_of_each_card)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
