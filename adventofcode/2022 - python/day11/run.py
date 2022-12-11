import sys
from pathlib import Path


def get_operand(s):
    if s == "old":
        return s
    return int(s)


def get_value(old, a):
    if a == "old":
        return old
    return int(a)


def get_op(a, b, kind):
    if kind == "+":
        return lambda old: get_value(old, a) + get_value(old, b)
    elif kind == "*":
        return lambda old: get_value(old, a) * get_value(old, b)
    raise NotImplementedError


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    monkeys = []
    content = content.split("\n")
    for i in range(0, len(content), 7):
        raw_items = content[i + 1][len("  Starting items: ") :].split(", ")
        items = list(map(int, raw_items))
        operation = content[i + 2][len("  Operation: new = ") :]
        if len(s := operation.split(" + ")) == 2:
            op = get_op(s[0], s[1], "+")
        elif len(s := operation.split(" * ")) == 2:
            op = get_op(s[0], s[1], "*")
        else:
            raise ValueError(f"operation: {operation} not understood")
        # Test
        divisor = int(content[i + 3].split(" ")[-1])
        if_true = int(content[i + 4].split(" ")[-1])
        if_false = int(content[i + 5].split(" ")[-1])
        monkeys.append(
            dict(items=items, op=op, divisor=divisor, if_false=if_false, if_true=if_true)
        )

    return monkeys


def main(monkeys, second_part):
    print("monkeys", monkeys)
    activity = [0] * len(monkeys)
    lcm = 1
    for monkey in monkeys:
        lcm *= monkey["divisor"]
    for r in range(10_000 if second_part else 20):
        for i, monkey in enumerate(monkeys):
            for worry in monkey["items"]:
                worry = monkey["op"](worry)
                if second_part:
                    # take the value modulo the least common multiple
                    # so number size is constrained
                    # the divisibility tests of the worry levels are not
                    # affected by property of the LCM.
                    worry = worry % lcm
                else:
                    worry = worry // 3
                if (worry % monkey["divisor"]) == 0:
                    monkeys[monkey["if_true"]]["items"].append(worry)
                else:
                    monkeys[monkey["if_false"]]["items"].append(worry)
                activity[i] += 1
            monkey["items"] = []
        if r % 1000 == 0:
            print(f"{r=}, activity={activity}")
        # for i, monkey in enumerate(monkeys):
        #     print("i", monkey["items"])

    a, b = sorted(activity, reverse=True)[:2]
    return a * b


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    print(f"result: {main(input_, second_part)}", file=sys.stdout)
