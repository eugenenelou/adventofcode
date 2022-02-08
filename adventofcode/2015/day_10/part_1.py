import sys


def look_and_say(s):
    current = None
    i = 0
    result = ""
    for c in s:
        if c == current:
            i += 1
        else:
            if current is not None and i:
                result += f"{i}{current}"
            current = c
            i = 1
    result += f"{i}{current}"
    return result


def main(input):
    s = next(iter(input)).rstrip()
    for _ in range(40):
        s = look_and_say(s)
    return len(s)


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
