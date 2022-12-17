import re
import sys
from pathlib import Path
import time
from itertools import product

input_regex = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+);[^A-Z]*([A-Z,][A-Z, ]+)")


def parse_input(path: str, second_part=False):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    valves = []
    for line in content.split("\n"):
        match = input_regex.match(line)
        valves.append((match.group(1), match.group(2), match.group(3).split(", ")))
    flows = {}
    paths = {}
    for from_, flow, tos in valves:
        flows[from_] = int(flow)
        paths[from_] = tos
    return flows, paths


def main1(flows, paths):
    MAX_TIME = 30
    start = "START"
    first_valve = "AA"
    distances = {}
    # compute the distance between each pair of valves

    def compute_distance(from_valve, current_valve, visited_valves):
        for next_valve in paths[current_valve]:
            if next_valve not in visited_valves:
                visited_valves.add(next_valve)
                pair = (from_valve, next_valve)
                reverse_pair = (next_valve, from_valve)
                dist = len(visited_valves)
                if pair not in distances or dist < distances[pair]:
                    distances[pair] = dist
                    distances[reverse_pair] = dist
                compute_distance(from_valve, next_valve, visited_valves)
                visited_valves.remove(next_valve)

    for valve in paths:
        # slow, can be optimized
        print("computing distances starting from", valve)
        compute_distance(valve, valve, set())

    for valve in paths:
        if valve != first_valve:
            distances[(start, valve)] = distances[(first_valve, valve)]
    distances[(start, first_valve)] = 0

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
                yield from get_pressure_paths(
                    valve,
                    t + distance + 1,
                    accumulated_pressure + valve_total_pressure,
                    [*acc, (valve, t + distance + 1, valve_total_pressure)],
                )
                open_valves[valve] = False

        if not found_valves:
            yield accumulated_pressure

    return max(get_pressure_paths(start, t=0, acc=[]))


def main2(flows, paths):
    MAX_TIME = 26
    start = "START"
    first_valve = "AA"
    distances = {}
    # compute the distance between each pair of valves

    def compute_distance(from_valve, current_valve, visited_valves):
        for next_valve in paths[current_valve]:
            if next_valve not in visited_valves:
                visited_valves.add(next_valve)
                pair = (from_valve, next_valve)
                reverse_pair = (next_valve, from_valve)
                dist = len(visited_valves)
                if pair not in distances or dist < distances[pair]:
                    distances[pair] = dist
                    distances[reverse_pair] = dist
                compute_distance(from_valve, next_valve, visited_valves)
                visited_valves.remove(next_valve)

    for valve in paths:
        # slow, can be optimized
        print("computing distances starting from", valve)
        compute_distance(valve, valve, set())

    for valve in paths:
        if valve != first_valve:
            distances[(start, valve)] = distances[(first_valve, valve)]
    distances[(start, first_valve)] = 0

    open_valves = {valve: False for valve in paths if flows[valve] > 0}

    def get_pressure_paths(open_valves, current_valve, t, accumulated_pressure=0):
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
                yield from get_pressure_paths(
                    open_valves,
                    valve,
                    t + distance + 1,
                    accumulated_pressure + valve_total_pressure,
                )
                open_valves[valve] = False

        if not found_valves:
            yield accumulated_pressure

    def split_valves(valves, min_size=5):
        # This does  twice too  many split, because the problem is symmetrical
        # so we can stop at half because the product is symmetrical
        n = len(valves)
        half_possibilities = 2 ** (n - 1)
        for i, split in zip(range(half_possibilities), product((False, True), repeat=len(valves))):
            print("i", i)
            my_valves = {}
            elephant_valves = {}
            s = sum(split)
            if s < min_size:  # assume more than min_size valves are open by each party
                continue
            for valve, mine in zip(valves, split):
                if mine:
                    my_valves[valve] = False
                else:
                    elephant_valves[valve] = False
            yield my_valves, elephant_valves

    # this takes ~80s
    return max(
        max(get_pressure_paths(my_valves, start, t=0))
        + max(get_pressure_paths(elephant_valves, start, t=0))
        for my_valves, elephant_valves in split_valves(list(open_valves.keys()))
    )


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath, second_part=second_part)
    start_time = time.time()
    if second_part:
        print(f"result: {main2(*input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(*input_)}", file=sys.stdout)
    end_time = time.time()
    print(f"It took {end_time - start_time:02f}s")
