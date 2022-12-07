import sys
from pathlib import Path
from functools import lru_cache

from pprint import pprint


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    current_id = None
    inodes = {}
    idx = 0

    def get_idx():
        nonlocal idx
        idx += 1
        return idx

    for line in content.split("\n"):
        if line.startswith("$"):
            if line.startswith("$ cd"):
                cmd = line.split(" ")[-1]
                if cmd == "..":
                    current_id = inodes[current_id]["parent"]
                else:
                    if current_id is None:  # init
                        new_id = f"{get_idx()}_{cmd}"
                        inodes[new_id] = {
                            "type": "dir",
                            "parent": current_id,
                            "name": cmd,
                            "size": None,
                            "subdirs": {},
                            "files": [],
                        }
                        current_id = new_id
                    elif cmd in inodes[current_id]["subdirs"]:
                        current_id = inodes[current_id]["subdirs"][cmd]
                    else:
                        raise Exception("ls should set the value before this")
        else:
            a, b = line.split(" ")
            if a == "dir":
                id_ = f"{get_idx()}_{b}"
                inodes[id_] = {
                    "type": "dir",
                    "parent": current_id,
                    "name": b,
                    "size": None,
                    "subdirs": {},
                    "files": [],
                }
                inodes[current_id]["subdirs"][b] = id_
            else:
                id_ = f"{get_idx()}_{b}"
                inodes[id_] = {"type": "file", "size": int(a), "name": b}
                inodes[current_id]["files"].append(id_)
    return inodes


def get_root_id(inodes):
    return next(id_ for id_, inode in inodes.items() if inode["parent"] is None)


def compute_sizes(inodes):
    root_id = get_root_id(inodes)

    @lru_cache
    def inner(current_id):
        inode = inodes[current_id]
        size = sum(inner(subdir) for subdir in inode["subdirs"].values()) + sum(
            inodes[file]["size"] for file in inode["files"]
        )
        inodes[current_id]["size"] = size
        return size

    inner(root_id)


def main1(inodes):
    compute_sizes(inodes)

    return sum(
        inode["size"]
        for inode in inodes.values()
        if inode["size"] <= 100_000 and inode["type"] == "dir"
    )


def main2(inodes):
    compute_sizes(inodes)
    root_id = get_root_id(inodes)

    total_size = inodes[root_id]["size"]
    min_space_to_get = total_size - 40_000_000

    sizes = [inode["size"] for inode in inodes.values() if inode["type"] == "dir"]

    return next(size for size in sorted(sizes) if size >= min_space_to_get)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
