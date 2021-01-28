import collections
import re

test_inputs = [
    "inputs/day4"
]

log_pattern = re.compile(r"\[([0-9\-]+)\s+(\d+):(\d+)\]\s*(.*)")


class Event:
    def __init__(self, date, hour, minute, desc):
        self.date = date
        self.hour = hour
        self.minute = minute
        self.desc = desc

    def __str__(self):
        return "[{} {}:{}] {}".format(
            self.date, self.hour, self.minute, self.desc)

    def __repr__(self):
        return str(self)


def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return Event(
            match.group(1),
            int(match.group(2)),
            int(match.group(3)),
            match.group(4))


def solve(events):
    asleep = collections.defaultdict(lambda: collections.defaultdict(int))
    current_guard = None
    last_sleep = None
    for event in events:
        if event.desc.startswith("Guard"):
            parts = event.desc.split()
            gid = int(parts[1].replace("#", ""))
            current_guard = gid
        elif event.desc.startswith("falls asleep"):
            last_sleep = event
        elif event.desc.startswith("wakes up"):
            for m in range(last_sleep.minute, event.minute):
                asleep[current_guard][m] += 1

    summary = []
    for k in asleep:
        total_sleep = sum(asleep[k].values())
        most_slept = max(asleep[k].items(), key=lambda i: i[1])
        summary.append((total_sleep, most_slept, k))

    p1 = max(summary, key=lambda s: s[0])
    p1_result = p1[1][0] * p1[2]

    p2 = max(summary, key=lambda s: s[1][1])
    p2_result = p2[1][0] * p2[2]
    return p1_result, p2_result


def process(path):
    print("Input:", path)
    with open(path) as f:
        events = [parse_log_line(line) for line in f]
        events.sort(key=lambda e: (e.date, e.hour, e.minute))
        print(solve(events))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
