import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    rows = content.split("\n")
    empty_rows = [all(char == "." for char in row) for row in rows]
    empty_columns = [all(row[i] == "." for row in rows) for i in range(len(rows[0]))]
    galaxies = [
        (i, j)
        for i, row in enumerate(rows)
        for j, char in enumerate(row)
        if char == "#"
    ]
    return empty_rows, empty_columns, galaxies


def main1(input_, expand=1):
    empty_rows, empty_columns, galaxies = input_
    res = 0
    for i, (x1, y1) in enumerate(galaxies):
        for j, (x2, y2) in enumerate(galaxies[i + 1 :]):
            a, b = (x1, x2) if x1 <= x2 else (x2, x1)
            c, d = (y1, y2) if y1 <= y2 else (y2, y1)
            dist = (
                (b - a)
                + (d - c)
                + sum(empty_rows[a + 1 : b]) * expand
                + sum(empty_columns[c + 1 : d]) * expand
            )
            # print(f"galaxy {i+1} and galaxy {i+j+2}, {dist=}")
            res += dist
    return res


def main2(input_):
    return main1(input_, expand=999_999)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
