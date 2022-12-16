import re
import sys
from pathlib import Path
from tkinter import N

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
        flows[from_] = int(flow)
        paths[from_] = tos
    return flows, paths


MAX_TIME = 30

def main1(flows, paths, max_t = 30):
    start = "START"
    first_valve = "AA"
    distances = {}
    # compute the distance between each pair of valves
    seen = None
    print('# Paths')
    print(paths, end='\n\n')
    print(paths['TG'])
    print(paths['AV'])
    print(paths['AX'])
    def compute_distance(from_valve, current_valve, offset=1):
        if from_valve in ('TG', 'AX'):
            print('current', from_valve, current_valve, offset, seen)
        next_valves = []
        for next_valve in paths[current_valve]:
            if next_valve not in seen and next_valve != from_valve:
                seen.add(next_valve)
                pair = (from_valve, next_valve)
                if pair not in distances or offset < distances[pair]:
                    if pair == ('TG', 'AV'):
                        print(offset, from_valve, current_valve, next_valve, distances.get(pair))
                    distances[pair] = offset
                    next_valves.append(next_valve)

        for next_valve in next_valves:
            compute_distance(from_valve, next_valve, offset+1)

    for valve in paths:
        seen = set()
        compute_distance(valve, valve)

    for valve in paths:
        if valve != first_valve:
            distances[(start, valve)] = distances[(first_valve, valve)]
    distances[(start, first_valve)] = 0

    for (p1, p2), v in list(distances.items()):
        p = (p2, p1)
        if p not in distances:
            distances[p] = v

    # print('# Distances')
    # for d, v in distances.items():
    #         print(d, v)

    # Check that all distances are in both directions
    for (p1, p2), v in distances.items():
        assert p1 == start or distances[(p2, p1)] == v, ((p1, p2), distances[(p2, p1)], v)

    open_valves = {valve: False for valve in paths if flows[valve] > 0}

    def get_pressure_paths(current_valve, t, accumulated_pressure=0, acc=None):
        found_valves = False
        remaining_time = MAX_TIME - t
        for valve, is_open in open_valves.items():
            if is_open:
                continue
            distance = distances[(current_valve, valve)]
            if distance < remaining_time:
                found_valves = True
                open_valves[valve] = True
                valve_total_pressure = (remaining_time - distance - 1) * flows[valve]
                yield from get_pressure_paths(valve, t + distance + 1, accumulated_pressure+valve_total_pressure, [*acc, (valve, valve_total_pressure)])
                open_valves[valve] = False

        if not found_valves:
            # print(acc, accumulated_pressure)
            # if accumulated_pressure == 1667:
            #     print(acc)
            # if [v for v, _ in acc] == ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']:
            #     print(acc, accumulated_pressure)
            yield accumulated_pressure

    return max(get_pressure_paths(start, t=0, acc = []))


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
