from socket import IPV6_V6ONLY
import sys

voyels = "aeiou"

forbidden_doubles = ["ab", "cd", "pq", "xy"]


def main(input):
    count = 0
    for s in input:
        voyels_count = 0
        has_double = False
        failed = False
        if s[0] in voyels:
            voyels_count += 1
        for i in range(len(s) - 1):
            c1, c2 = s[i : i + 2]
            if f"{c1}{c2}" in forbidden_doubles:
                failed = True
                break
            if c1 == c2:
                has_double = True
            if c2 in voyels:
                voyels_count += 1
        if not failed and voyels_count >= 3 and has_double:
            count += 1

    return count


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
