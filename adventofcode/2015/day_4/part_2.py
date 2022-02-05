import sys
import hashlib


def hash(key, i):
    return hashlib.md5(f"{key}{i}".encode()).hexdigest()


def main(input):
    key = next(iter(input)).rstrip()
    print("key", f"'{key}'")
    i = 0
    result = hash(key, i)
    while result[:6] != "000000":
        i += 1
        result = hash(key, i)
    return i


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
