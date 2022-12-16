import re
import sys
from pathlib import Path

input_regex = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+);[^A-Z]*([A-Z,][A-Z, ]+)")


def parse_input(path: str, second_part = False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    valves = []
    for line in content.split('\n'):
        match = input_regex.match(line)
        valves.append((match.group(1), match.group(2), match.group(3).split(', ')))
    flows = {}
    paths = {}
    for from_, flow, tos in valves:
        flows[from_] = flow
        paths[from_] = tos
    return flows, paths


def main1(flows, paths, max_t = 30):
    distances = {}
    first_valve = "AA"
    # compute the distance between each pair of valves

    def compute_distance(from_valve, current_valve, offset=0):
        if offset > 0:
            distances[(from_valve, current_valve)] = offset
            distances[(current_valve, from_valve)] = offset
        for next_valve in paths[current_valve]:
            if (from_valve, next_valve) not in distances:
                compute_distance(from_valve, next_valve, offset+1)

    for valve in paths:
        compute_distance(valve, valve)

    open_valves = {valve: False for valve in paths}


    # for valve, next_valves in paths.items():
    #     for next_valve in next_valves:
    #         distances[(valve, next_valve)] = 1
    #         distances[(next_valve, valve)] = 1

    # def yield_possible_paths():

    # return max(yield_possible_paths())

def main2(input_):
    return 0


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath, second_part=second_part)
    if second_part:
        print(f"result: {main2(*input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(*input_)}", file=sys.stdout)
