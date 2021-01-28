import collections
import re
from queue import PriorityQueue

test_inputs = [
    "inputs/day7"
]

line_pattern = re.compile(r"Step\s*(\w*)\s+must.*step\s+(\w*)\s+can.*")


def interpret(rules):
    pred = collections.defaultdict(set)
    succ = collections.defaultdict(set)
    domain = set()
    for rule in rules:
        pred[rule[1]].add(rule[0])
        succ[rule[0]].add(rule[1])
        domain.add(rule[0])
        domain.add(rule[1])
    return pred, succ, domain


def part1(rules):
    pred, succ, domain = interpret(rules)
    available = set(s for s in domain if len(pred[s]) == 0)
    result = ""
    while available:
        item = min(available)
        result += item
        available.remove(item)
        domain.remove(item)
        for s in succ[item]:
            pred[s].remove(item)
            if len(pred[s]) == 0:
                available.add(s)
    return result


def time(task):
    return ord(task) - ord('A') + 61


def part2(rules, workers):
    clock = 0
    jobs = {}
    available = PriorityQueue()
    pred, succ, domain = interpret(rules)
    for task in domain:
        if len(pred[task]) == 0:
            available.put(task)
    while not available.empty() or jobs:
        capacity = workers - len(jobs)
        while capacity > 0 and not available.empty():
            task = available.get()
            jobs[task] = time(task)
            capacity -= 1
        step = min(jobs.values())
        clock += step
        for task in list(jobs.keys()):
            jobs[task] -= step
            if jobs[task] == 0:
                for s in succ[task]:
                    pred[s].remove(task)
                    if len(pred[s]) == 0:
                        available.put(s)
                del jobs[task]
    return clock


def parse_line(line):
    match = line_pattern.match(line)
    if match:
        return match.group(1), match.group(2)
    return None


def process(path):
    with open(path) as f:
        rules = [parse_line(line) for line in f]
        print(part1(rules))
        print(part2(rules, 5))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
