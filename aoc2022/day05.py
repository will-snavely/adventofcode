import re
import collections

def read_stacks():
    stacks = collections.defaultdict(list)
    with open("inputs/day05_stacks") as f:
        lines = [x.strip() for x in f.readlines()]
        for line in lines:
            count = 0
            for match in re.finditer(r'[A-Z]', line):
                idx = match.start() // 4
                stacks[idx].insert(0, match.group())
    return stacks

def part1(stacks, commands):
    for command in commands:
        amt, start, end = command
        for _ in range(amt):
            stacks[end].append(stacks[start].pop())
    return stacks

def part2(stacks, commands):
    for command in commands:
        amt, start, end = command
        stacks[end] += stacks[start][-amt:]
        stacks[start] = stacks[start][:-amt]
    return stacks

if __name__ == "__main__":
    commands = []
    with open("inputs/day05") as f:
        lines = [x.strip() for x in f.readlines()]
        for line in lines:
            match = re.search(r'move (\d*) from (\d*) to (\d*)', line)
            amt = int(match.groups()[0])
            start = int(match.groups()[1]) - 1
            end = int(match.groups()[2]) - 1
            commands.append([amt, start, end])

    p1_stacks = part1(read_stacks(), commands)
    p1 = ""
    for idx in range(len(p1_stacks.keys())):
        p1 += p1_stacks[idx][-1]
    print(p1)

    p2_stacks = part2(read_stacks(), commands)
    p2 = ""
    for idx in range(len(p2_stacks.keys())):
        p2 += p2_stacks[idx][-1]
    print(p2)

