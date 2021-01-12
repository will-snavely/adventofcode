import collections

test_inputs = [
    "inputs/day6"
]


def build_orbit_graph(rules):
    children = collections.defaultdict(list)
    parent = {}
    for rule in rules:
        parts = rule.split(")")
        children[parts[0]].append(parts[1])
        parent[parts[1]] = parts[0]
    return children, parent


def count_orbits(children, node, depth):
    result = depth
    for neighbor in children[node]:
        result += count_orbits(children, neighbor, depth + 1)
    return result


def path_to_root(parent, start):
    path = [start]
    cur = start
    while cur != "COM":
        cur = parent[cur]
        path.append(cur)
    return path


def process(path):
    print("Input:", path)
    with open(path) as f:
        rules = [line.strip() for line in f.readlines()]
        children, parent = build_orbit_graph(rules)
        print("\tPart 1:", count_orbits(children, "COM", 0))

        you_path = path_to_root(parent, "YOU")
        santa_path = path_to_root(parent, "SAN")
        santa_nodes = set(santa_path)
        ancestor = None
        for node in you_path:
            if node in santa_nodes:
                ancestor = node
                break
        you_dist = you_path.index(ancestor)
        santa_dist = santa_path.index(ancestor)
        print("\tPart 2:", you_dist + santa_dist - 2)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
