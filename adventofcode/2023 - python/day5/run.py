import sys
from bisect import bisect_right
from operator import itemgetter
from pathlib import Path


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    raw_seeds, *raw_mappings = content.split("\n\n")
    seeds = [int(seed) for seed in raw_seeds.split(": ", maxsplit=1)[1].split()]
    mappings = []
    for raw_mapping in raw_mappings:
        ranges = []
        for row in raw_mapping.split("\n")[1:]:
            destination, source, range_size = map(int, row.split())
            ranges.append((source, destination, range_size))
        ranges.sort(key=itemgetter(0))
        mappings.append(ranges)
    return seeds, mappings


def get_seed_location(seed, mappings):
    id_ = seed
    for mapping in mappings:
        idx = bisect_right(mapping, id_, key=itemgetter(0))
        source, destination, range_size = mapping[idx - 1]
        delta = id_ - source
        if delta <= range_size and idx > 0:
            id_ = destination + delta
    return id_


def main1(input_):
    seeds, mappings = input_
    return min(get_seed_location(seed, mappings) for seed in seeds)


def get_mapping(
    id_: int, range_size: int, mapping: list[tuple[int, int, int]], acc=tuple()
) -> list[tuple[int, int]]:
    idx = bisect_right(mapping, id_, key=itemgetter(0))
    source, destination, new_range_size = mapping[idx - 1]
    delta = id_ - source
    if idx == len(mapping) and delta >= new_range_size:
        return [*acc, (id_, range_size)]
    if delta >= new_range_size or idx == 0:
        # below the lowest interval start or strictly between 2 intervals
        new_id = id_
        source, destination, new_range_size = mapping[idx]
        if -delta >= range_size:
            return [*acc, (new_id, range_size)]
        else:
            return get_mapping(
                source,
                range_size + delta,
                mapping,
                [*acc, (id_, -delta)],
            )
    else:
        # found a matching interval start
        new_id = destination + delta
        if delta + range_size <= new_range_size:
            return [*acc, (new_id, range_size)]
        return get_mapping(
            source + new_range_size,
            range_size - new_range_size + delta,
            mapping,
            [*acc, (new_id, new_range_size - delta)],
        )


def main2(input_):
    seeds, mappings = input_
    location_ranges = []
    for i in range(0, len(seeds), 2):
        ranges = [seeds[i : i + 2]]
        for j, mapping in enumerate(mappings):
            new_ranges = []
            for seed, range_size in ranges:
                new_ranges.extend(get_mapping(seed, range_size, mapping))
            ranges = new_ranges
        location_ranges.extend(ranges)
    return min(seed for seed, _ in location_ranges)


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
