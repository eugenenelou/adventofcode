import sys


def parse_input(input):
    reindeers = {}
    for instruction in input:
        words = instruction.split(" ")
        reindeers[words[0]] = {
            "speed": int(words[3]),
            "duration": int(words[6]),
            "rest": int(words[13]),
        }
    return reindeers


def simulate(n, reindeer):
    interval_dist = reindeer["speed"] * reindeer["duration"]
    interval_dur = reindeer["duration"] + reindeer["rest"]
    return interval_dist * (n // interval_dur) + reindeer["speed"] * min(
        reindeer["duration"], n % interval_dur
    )


def main1(input):
    input = iter(input)
    n = int(next(input).rstrip())
    reindeers = parse_input(input)
    return max(simulate(n, reindeer) for reindeer in reindeers.values())


def dist_each_second(reindeer, total_time):
    time = 0
    interval = 0
    rest = False
    dist = 0
    while time < total_time:
        time += 1
        interval += 1
        if rest:
            if interval == reindeer["rest"]:
                rest = False
                interval = 0
            yield dist
        else:
            dist += reindeer["speed"]
            yield dist
            if interval == reindeer["duration"]:
                rest = True
                interval = 0


def main2(input):
    input = iter(input)
    n = int(next(input).rstrip())
    reindeers = parse_input(input)
    scores = [0] * len(reindeers)
    for distances in zip(*(dist_each_second(reindeer, n) for reindeer in reindeers.values())):
        maxi = max(distances)
        for i, value in enumerate(distances):
            if value == maxi:
                scores[i] += 1
    return max(scores)


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
