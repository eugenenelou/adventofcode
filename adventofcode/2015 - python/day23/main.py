import sys


def parse_input(input_):
    for line in input_:
        line = line.rstrip()
        if line.startswith("jio"):
            r, offset = line[4:].split(", ")
            yield "jio", r, int(offset)
        elif line.startswith("jie"):
            r, offset = line[4:].split(", ")
            yield "jie", r, int(offset)
        elif line.startswith("jmp "):
            yield "jmp", int(line[4:])
        else:
            yield line.split(" ")


def main(commands, a=0, b=0):
    registries = dict(a=a, b=b)

    i = 0
    n = len(commands)
    while 0 <= i < n:
        command = commands[i]
        instruction = command[0]
        if instruction == "hlf":
            r = command[1]
            registries[r] = registries[r] // 2
            i += 1
        elif instruction == "tpl":
            r = command[1]
            registries[r] = registries[r] * 3
            i += 1
        elif instruction == "inc":
            r = command[1]
            registries[r] += 1
            i += 1
        elif instruction == "jmp":
            offset = command[1]
            i += offset
        elif instruction == "jie":
            r, offset = command[1:]
            i += offset if registries[r] % 2 == 0 else 1
        elif instruction == "jio":
            r, offset = command[1:]
            i += offset if registries[r] == 1 else 1
    print(f"{i=}, a={registries['a']}, b={registries['b']}")

    return registries["b"]


if __name__ == "__main__":
    input_ = sys.stdin
    second_part = "--two" in sys.argv
    input_ = list(parse_input(input_))

    if second_part:
        print(main(input_, a=1), file=sys.stdout)
    else:
        print(main(input_), file=sys.stdout)
