import collections
from typing import NamedTuple


class Pt(NamedTuple('Pt', [('x', int), ('y', int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)


deltas = {"N": Pt(-1, 0), "S": Pt(1, 0), "E": Pt(0, 1), "W": Pt(0, -1)}


def distances(start, graph):
    queue = collections.deque()
    seen = set()
    queue.append((start, 0))
    while queue:
        p, dist = queue.popleft()
        yield dist, p
        for adj in graph[p]:
            if adj not in seen:
                seen.add(adj)
                queue.append((adj, dist + 1))


def build_graph(regex):
    positions = {Pt(0, 0)}
    positions_before_branch = []
    positions_reached_in_branch = []
    graph = collections.defaultdict(set)
    for c in regex:
        if c in deltas:
            update = set()
            for p in positions:
                q = p + deltas[c]
                graph[p].add(q)
                graph[q].add(p)
                update.add(q)
            positions = update
        elif c == "(":
            # When we hit a fork, we need to save the current
            # set of positions so that we can backtrack on "|"
            positions_before_branch.append(positions)

            # We also need to keep track of all the positions reached
            # in each branch of the fork. When the fork concludes this
            # will become our new position set
            positions_reached_in_branch.append(set())
        elif c == "|":
            # Backtrack to our position set at the beginning of the fork
            positions_reached_in_branch[-1].update(positions)
            positions = positions_before_branch[-1]
        elif c == ")":
            positions_reached_in_branch[-1].update(positions)
            positions = positions_reached_in_branch.pop()
            positions_before_branch.pop()
    return graph


def main():
    with open("inputs/day20") as f:
        regex = f.read()
    graph = build_graph(regex)
    print(max(distances(Pt(0, 0), graph)))
    print(len(list(filter(lambda d: d[0] >= 1000, distances(Pt(0, 0), graph)))))


if __name__ == "__main__":
    main()
