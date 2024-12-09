import sys
from pathlib import Path


def parse_input(path: str) -> tuple[list[int], list[int]]:
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content


def main1(input_):
    blocks = [(i, int(block)) for i, block in enumerate(input_[::2])]
    holes = [int(hole) for hole in input_[1::2]]
    forward_blocks = iter(blocks)
    reversed_blocks = iter(reversed(blocks))

    res = 0
    idx = 0

    last_file_id, remaining_cells = next(reversed_blocks)

    def hash(file_id, count=1):
        nonlocal res, idx
        for _ in range(count):
            res += file_id * idx
            # print("hash", idx, "*", file_id, "=", res)
            idx += 1

    in_block = True  # if false: filling hole
    first_file_id, count = next(forward_blocks)
    holes_iter = iter(holes)
    hole = next(holes_iter)
    while first_file_id < last_file_id:  # TODO
        if in_block:
            hash(first_file_id, count)
            first_file_id, count = next(forward_blocks)
            in_block = False
        else:
            if hole == 0:
                hole = next(holes_iter)
            if remaining_cells > hole:
                hash(last_file_id, hole)
                remaining_cells -= hole
                hole = 0
                in_block = True
            elif hole > remaining_cells:
                hash(last_file_id, remaining_cells)
                hole -= remaining_cells
                last_file_id, remaining_cells = next(reversed_blocks)
            else:
                in_block = True
                hash(last_file_id, hole)
                hole = 0
                last_file_id, remaining_cells = next(reversed_blocks)
    if remaining_cells:
        hash(last_file_id, remaining_cells)
    return res


def main2(input_):
    start_idx = 0
    data = []
    for i, cell in enumerate(input_):
        data.append((i // 2 if i % 2 == 0 else None, int(cell), start_idx))
        start_idx += int(cell)

    total = 0

    def hash(file_id, start_idx, file_size):
        nonlocal total
        s = 0
        for i in range(file_size):
            s += start_idx + i
        total += file_id * s

    data_len = len(data)
    for i in range(data_len - 1, -1, -2):
        file_id, file_size, _ = data[i]
        for j in range(1, i, 2):
            _, hole_size, start_idx = data[j]
            if hole_size < file_size:
                continue
            else:
                hash(file_id, start_idx, file_size)
                data[j] = (None, hole_size - file_size, start_idx + file_size)
                data[i] = (file_id, 0, 0)
                # collapse the holes
                try:
                    next_hole_size = data[i + 1][1]
                    data[i + 1] = (None, 0, 0)
                except IndexError:
                    next_hole_size = 0
                data[i - 1] = (
                    None,
                    data[i - 1][1] + file_size + next_hole_size,
                    data[i - 1][2],
                )
                break
    for file_id, file_size, start_idx in data:
        if file_id is None:
            continue
        hash(file_id, start_idx, file_size)
        start_idx += file_size
    return total


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
