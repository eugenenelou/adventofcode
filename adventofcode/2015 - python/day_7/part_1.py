import sys

bitmask = 2**16 - 1


def main(input):
    wire_instructions = {}
    wire_values = {}
    for instruction in input:
        match inst := instruction.rstrip().split(" "):
            case [w1, "AND", w2, "->", w3]:
                wire_instructions[w3] = (w1, w2, lambda v1, v2: v1 & v2)
            case [w1, "OR", w2, "->", w3]:
                wire_instructions[w3] = (w1, w2, lambda v1, v2: v1 | v2)
            case [w1, "LSHIFT", n, "->", w3]:
                # n must be passed as argument to the lambda otherwise the reference is bound
                # instead of the value
                wire_instructions[w3] = (w1, n, lambda v1, n: bitmask & (v1 << int(n)))
            case [w1, "RSHIFT", n, "->", w3]:
                wire_instructions[w3] = (w1, n, lambda v1, n: v1 >> int(n))
            case ["NOT", w1, "->", w3]:
                wire_instructions[w3] = (w1, lambda v1: 65535 ^ v1)
            case [w1, "->", w3]:
                wire_instructions[w3] = (w1, lambda v: v)
            case _:
                raise Exception(f"Instruction not understood: {inst}")

    def compute_value(w):
        match inst := wire_instructions[w]:
            case w1, w2, f:
                return f(get_value(w1), get_value(w2))
            case w1, f:
                return f(get_value(w1))
            case _:
                raise Exception(f"Instruction not understood: {inst}")

    def get_value(w):
        if w.isnumeric():
            return int(w)
        if w in wire_values:
            value = wire_values[w]
        else:
            value = wire_values[w] = compute_value(w)
        return value

    return get_value("a")


if __name__ == "__main__":
    input = sys.stdin
    print(main(input), file=sys.stdout)
