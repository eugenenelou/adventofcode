import sys
from pathlib import Path


def parse_input(path: str):
    return Path(path).read_text()


def start_of_packet(chars, n):
    return len(set(chars)) == n


def main(input_, n):
    for i in range(len(input_) - n + 1):
        if start_of_packet(input_[i : i + n], n):
            return i + n


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    print(f"result: {main(input_, n=14 if second_part else 4)}", file=sys.stdout)
