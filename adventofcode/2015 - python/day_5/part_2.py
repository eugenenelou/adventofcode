from socket import IPV6_V6ONLY
import sys


def main(input):
    count = 0
    for s in input:
        doubles_indexes = {(s[0], s[1]): 0}
        sandwich = False
        double_double = False
        for i in range(1, len(s) - 1):
            c1, c2, c3 = s[i - 1 : i + 2]
            if c1 == c3:
                sandwich = True

            if (c2, c3) in doubles_indexes:
                if doubles_indexes[(c2, c3)] < i - 1:
                    double_double = True
            else:  # don't override a lefter double, when the current one could overlap
                doubles_indexes[(c2, c3)] = i

            if sandwich and double_double:
                break

        if sandwich and double_double:
            count += 1

    return count


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
