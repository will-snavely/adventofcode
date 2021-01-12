import re


def parse_rule(text):
    match = re.match("(.*)contain(.*)", text)
    if match:
        lhs = match.group(1).replace("bags", "").strip()
        rhs = match.group(2).strip().strip(".")
        contains = {}
        if rhs != "no other bags":
            for item in rhs.split(","):
                stripped = item.strip()
                parts = stripped.split(None, 1)
                amt = int(parts[0])
                color = parts[1].replace("bags", "").replace("bag", "").strip()
                contains[color] = amt
        return lhs, contains


def traverse(graph, start, end, can_reach, visited):
    visited.add(start)
    neighbors = graph[start].keys()

    if end in neighbors:
        can_reach.add(start)
        return True

    for neighbor in neighbors:
        if neighbor in visited:
            continue
        if traverse(graph, neighbor, end, can_reach, visited):
            can_reach.add(start)
            return True
    return False


def compute_reachability(graph, end):
    colors = graph.keys()
    can_reach = set()

    for color in colors:
        if color in can_reach:
            continue
        print(color)
        traverse(graph, color, end, can_reach, set())
    print(len(can_reach))


def count_bags(graph, node, visited, level):
    print("\t" * level, node)
    result = 0
    for color, count in graph[node].items():
        result += count * count_bags(graph, color, visited, level + 1) + count
    return result


def main():
    graph = {}
    with open("inputs/day7") as f:
        for line in f:
            color, contains = parse_rule(line)
            if color in graph:
                print("Weird, color already there:", color)
            graph[color] = contains
        # compute_reachability(graph, "shiny gold")
        print(count_bags(graph, "shiny gold", set(), 0))


if __name__ == "__main__":
    main()
