import sys
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split(",")


def hash_(value: str):
    res = 0
    for char in value:
        res = ((res + ord(char)) * 17) % 256
    return res


def main1(input_):
    return sum(map(hash_, input_))


def main2(input_):
    boxes = [{} for _ in range(256)]
    for instruction in input_:
        if instruction.endswith("-"):
            label = instruction[:-1]
            boxes[hash_(label)].pop(label, None)
        elif "=" in instruction:
            label, focal_l = instruction.split("=")
            box = boxes[hash_(label)]
            if label in box:
                box[label] = int(focal_l)
            else:
                box[label] = int(focal_l)
        else:
            raise ValueError(f"{instruction=}")
    return sum(
        (box_idx + 1) * (lens_idx + 1) * focal_l
        for box_idx, box in enumerate(boxes)
        for lens_idx, focal_l in enumerate(box.values())
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
