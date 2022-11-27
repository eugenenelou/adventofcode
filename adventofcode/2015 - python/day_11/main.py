import sys
import string

letter_ranks = {l: i for i, l in enumerate(string.ascii_lowercase)}
i_value = letter_ranks["i"]
o_value = letter_ranks["o"]
l_value = letter_ranks["l"]


def rule1(pwd):
    for i in range(len(pwd) - 2):
        x, y, z = pwd[i : i + 3]
        if x + 2 == y + 1 == z:
            return True
    return False


def rule2_value(v):
    return not (v == i_value or v == o_value or v == l_value)


def rule2(pwd):
    return all(rule2_value(v) for v in pwd)


def rule3(pwd):
    pair = None
    l1 = pwd[0]
    for l2 in pwd[1:]:
        if l1 == l2:
            if l1 == pair:
                l1 = l2
                continue
            if pair is None:
                pair = l1
            else:
                return True
        l1 = l2
    return False


class Password:
    def __init__(self, values):
        self.values = values

    def is_valid(self):
        # rule2 is implemented by incr skipping the forbidden letters
        return rule1(self.values) and rule3(self.values)

    def incr(self):
        # skip the forbidden letters
        for i in range(len(self.values)):
            if not rule2_value(self.values[i]):
                # enough because i, o, l are not consecutive or the last letter
                self.values[i] += 1
                for j in range(i + 1, len(self.values)):
                    self.values[j] = 0
                return self

        # handle z increment
        i = -1
        self.values[i] += 1
        while self.values[i] >= 26:
            self.values[i] = 0
            i -= 1
            self.values[i] += 1
        return self

    @classmethod
    def from_string(cls, s):
        return cls([letter_ranks[c] for c in s])

    def __str__(self):
        return "".join(string.ascii_lowercase[v] for v in self.values)


def main1(input):
    password = Password.from_string(next(iter(input)).rstrip())
    while not password.is_valid():
        password.incr()
    return str(password)


def main2(input):
    password = Password.from_string("hepxxyzz").incr()
    while not password.is_valid():
        password.incr()
    return str(password)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
