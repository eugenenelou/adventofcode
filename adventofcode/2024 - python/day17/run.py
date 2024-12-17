import sys
from pathlib import Path
import re


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_registries, raw_program = content.split("\n\n")
    registries = [int(match.group(0)) for match in re.finditer(r"\d+", raw_registries)]
    program = [int(x) for x in raw_program.split(": ")[1].split(",")]
    return registries, program


def yield_solution(a: int, program: list[int]) -> list[int]:
    idx = 0
    registries = [a, 0, 0]
    program_len = len(program)

    def combo_operand(operand: int):
        if operand < 4:
            return operand
        if operand < 7:
            return registries[operand - 4]
        raise ValueError("Operand 7 is not valid")

    res = []
    while idx < program_len:
        op, operand = program[idx : idx + 2]
        match op:
            case 0:
                registries[0] = registries[0] // 2 ** combo_operand(operand)
            case 1:
                registries[1] = registries[1] ^ operand
            case 2:
                registries[1] = combo_operand(operand) % 8
            case 3:
                if registries[0] != 0:
                    idx = operand
                    continue
            case 4:
                registries[1] = registries[1] ^ registries[2]
            case 5:
                res.append(combo_operand(operand) % 8)
            case 6:
                registries[1] = registries[0] // 2 ** combo_operand(operand)
            case 7:
                registries[2] = registries[0] // 2 ** combo_operand(operand)
        idx += 2
    return res


def main1(input_):
    registries, program = input_
    res = yield_solution(registries[0], program)
    return ",".join(map(str, res))


OPS = [
    ("adv", True),
    ("bxl", False),
    ("bst", True),
    ("jnz", False),
    ("bxc", True),
    ("out", True),
    ("bdv", True),
    ("cdv", True),
]


registry_names = "ABC"


def print_program(program):
    for i in range(0, len(program), 2):
        op, operand = program[i : i + 2]
        op, is_combo = OPS[op]
        print(
            f"{op} {operand if not is_combo else (operand if operand < 4 else registry_names[operand-4])}",
            file=sys.stderr,
        )


def main2(input_):
    """
    Looking at the input algorithm, every round of the output is computed from
    the rest of A % 8, and each round A is divided by 8.
    the output also depends on the previous bits because C comes from A // 2**B where
    B is a number between 0 and 7.

    So the algorithm consist of finding the first bits of A, that will determine the last output
    then find the next bits of A determining the previous output, etc until we build the first number
    that match the expected output.
    Also if we don't find a number, we backtrack to the last choice we made, trying the next one.

    if the output is of size n, it and we require 3 bits per output, then the number order of magnitude
    is 8**n, that where we start looking for the digit trying 0*8**n, 1*8**n, etc.
    """
    program = input_[1]
    program_len = len(program)

    choices = []
    j = 0
    while (i := len(choices)) < program_len:
        a = sum(
            choice * (8 ** (program_len - i - 1)) for i, choice in enumerate(choices)
        )
        found = False
        while not found and j < 8:
            delta = 8 ** (program_len - i - 1)
            try:
                outs = yield_solution(a + j * delta, program)
            except ValueError:
                outs = []
            if (
                len(outs) == program_len
                and outs[program_len - i - 1] == program[program_len - i - 1]
            ):
                choices.append(j)
                a += j * delta
                found = True
                j = 0
            else:
                j += 1
        if not found:
            # backtrack to the last assumption
            while (j := choices.pop(-1) + 1) == 8:
                pass
    return a


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
