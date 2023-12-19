import sys
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path


class Transition(Enum):
    MIN = 0
    MAX = 1
    DONE = 2


@dataclass(frozen=True, slots=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def count(self) -> int:
        return self.x + self.m + self.a + self.s


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_transitions, raw_parts = content.split("\n\n")
    transitions = {}
    for raw_transition in raw_transitions.split("\n"):
        key, raw_conditions = raw_transition[:-1].split("{")
        transitions[key] = conditions = []
        for raw_condition in raw_conditions.split(","):
            if ":" in raw_condition:
                inequality, dest = raw_condition.split(":")
                if "<" in inequality:
                    attr, limit = inequality.split("<")
                    conditions.append(
                        (
                            attr,
                            dest,
                            Transition.MAX,
                            int(limit),
                        )
                    )
                else:
                    attr, limit = inequality.split(">")
                    conditions.append(
                        (
                            attr,
                            dest,
                            Transition.MIN,
                            int(limit),
                        )
                    )
            else:
                conditions.append((None, raw_condition, Transition.DONE, None))
    parts = []
    for raw_part in raw_parts.split("\n"):
        kwargs = {}
        for couple in raw_part[1:-1].split(","):
            attr, value = couple.split("=")
            kwargs[attr] = int(value)
        parts.append(Part(**kwargs))
    return transitions, parts


def main1(input_):
    transitions, parts = input_
    count = 0

    for part in parts:
        key = "in"
        while True:
            for attr, new_key, type_, limit in transitions[key]:
                match type_:
                    case Transition.DONE:
                        key = new_key
                        break
                    case Transition.MIN:
                        if getattr(part, attr) > limit:
                            key = new_key
                            break
                    case Transition.MAX:
                        if getattr(part, attr) < limit:
                            key = new_key
                            break
            if key == "A":
                count += part.count
                break
            elif key == "R":
                break
    return count


@dataclass(slots=True)
class MetaPart:
    x: [int, int]
    m: [int, int]
    a: [int, int]
    s: [int, int]
    key: str

    @property
    def count(self):
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )


def main2(input_):
    transitions, _ = input_
    count = 0

    meta_parts = [
        MetaPart(x=[1, 4000], m=[1, 4000], a=[1, 4000], s=[1, 4000], key="in")
    ]
    while meta_parts:
        meta_part = meta_parts.pop()
        for attr, new_key, type_, limit in transitions[meta_part.key]:
            match type_:
                case Transition.DONE:
                    if new_key == "A":
                        count += meta_part.count
                    elif new_key != "R":
                        meta_parts.append(replace(meta_part, key=new_key))
                    break
                case Transition.MIN:
                    mini, maxi = getattr(meta_part, attr)
                    if mini > limit:
                        if new_key == "A":
                            count += meta_part.count
                        elif new_key != "R":
                            meta_parts.append(replace(meta_part, key=new_key))
                        continue
                    elif maxi <= limit:
                        continue
                    else:
                        matching_part = replace(
                            meta_part, **{attr: [limit + 1, maxi]}, key=new_key
                        )
                        if new_key == "A":
                            count += matching_part.count
                        elif new_key != "R":
                            meta_parts.append(matching_part)
                        setattr(meta_part, attr, [mini, limit])
                case Transition.MAX:
                    mini, maxi = getattr(meta_part, attr)
                    if maxi < limit:
                        if new_key == "A":
                            count += meta_part.count
                        elif new_key != "R":
                            meta_parts.append(replace(meta_part, key=new_key))
                        continue
                    elif mini >= limit:
                        continue
                    else:
                        matching_part = replace(
                            meta_part, **{attr: [mini, limit - 1]}, key=new_key
                        )
                        if new_key == "A":
                            count += matching_part.count
                        elif new_key != "R":
                            meta_parts.append(matching_part)
                        setattr(meta_part, attr, [limit, maxi])
    return count


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
