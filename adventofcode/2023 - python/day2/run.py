import sys
from pathlib import Path


def parse_game(game: str) -> list[dict[str, int]]:
    res = []
    for handful in game.split(": ", maxsplit=1)[1].split("; "):
        colors = {}
        for count_color in handful.split(", "):
            count, color = count_color.split(" ")
            colors[color] = int(count)
        res.append(colors)
    return res


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [(idx + 1, parse_game(game)) for idx, game in enumerate(content.split("\n"))]


bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def main1(input_):
    res = 0
    for idx, game in input_:
        if all(
            count <= bag.get(color, 0)
            for handful in game
            for color, count in handful.items()
        ):
            res += idx
    return res


def main2(input_):
    res = 0
    for idx, game in input_:
        min_colors = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for handful in game:
            for color, count in handful.items():
                min_colors[color] = max(min_colors[color], count)
        res += min_colors["blue"] * min_colors["green"] * min_colors["red"]
    return res


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
