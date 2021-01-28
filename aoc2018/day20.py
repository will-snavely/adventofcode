import collections
import itertools
from typing import NamedTuple


class Pt(NamedTuple('Pt', [('x', int), ('y', int)])):
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)


deltas = {
    "N": Pt(-1, 0),
    "S": Pt(1, 0),
    "E": Pt(0, 1),
    "W": Pt(0, -1)
}


class Pattern:
    def __init__(self):
        pass


class PatternLeaf(Pattern):
    def __init__(self, string):
        super().__init__()
        self.string = string


class PatternJoin(Pattern):
    def __init__(self, *args):
        super().__init__()
        self.children = []
        self.children.extend(args)


class PatternBranch(Pattern):
    def __init__(self, *args):
        super().__init__()
        self.children = []
        self.children.extend(args)


def build_expression_tree(regex_iter, parent):
    string = ""
    children = []
    while True:
        try:
            char = next(regex_iter)
        except StopIteration:
            break
        if char == "^":
            continue
        elif char in set("NSEW"):
            string += char
        elif char == "(":
            children.append(PatternLeaf(string))
            string = ""
            branch = PatternBranch()
            build_expression_tree(regex_iter, branch)
            children.append(branch)
        elif char == "|":
            children.append(PatternLeaf(string))
            build_expression_tree(regex_iter, parent)
            break
        elif char in set(")$"):
            children.append(PatternLeaf(string))
            break

    if len(children) > 1:
        join = PatternJoin()
        join.children.extend(children)
        if parent:
            parent.children.append(join)
        else:
            return join
    else:
        if parent:
            parent.children.extend(children)
        else:
            return children[0]
    return None


def draw_tree(pattern: Pattern, depth):
    if isinstance(pattern, PatternLeaf):
        print("{}Leaf[{}]".format("\t" * depth, pattern.string))
    elif isinstance(pattern, PatternJoin):
        print("{}Join".format("\t" * depth))
        for child in pattern.children:
            draw_tree(child, depth + 1)
    elif isinstance(pattern, PatternBranch):
        print("{}Branch".format("\t" * depth))
        for child in pattern.children:
            draw_tree(child, depth + 1)


def enumerate(pattern: Pattern):
    results = []
    if isinstance(pattern, PatternLeaf):
        return [pattern.string]
    elif isinstance(pattern, PatternBranch):
        for c in pattern.children:
            results.extend(enumerate(c))
    elif isinstance(pattern, PatternJoin):
        for p in itertools.product(*[enumerate(c) for c in pattern.children]):
            results.append("".join(p))
    return results


def count(pattern: Pattern):
    if isinstance(pattern, PatternLeaf):
        return 1
    elif isinstance(pattern, PatternBranch):
        result = 0
        for child in pattern.children:
            result += count(child)
        return result
    elif isinstance(pattern, PatternJoin):
        result = 1
        for child in pattern.children:
            result *= count(child)
        return result


def delta(s):
    return (
        sum(deltas[c][0] for c in s),
        sum(deltas[c][1] for c in s)
    )


def distances(start, edges):
    queue = collections.deque()
    seen = set()
    queue.append((start, 0))
    while queue:
        p, dist = queue.popleft()
        yield dist, p
        for d in deltas.values():
            q = p + d
            e = tuple(sorted([p, q]))
            if e in edges and q not in seen:
                seen.add(q)
                queue.append((q, dist + 1))


def build_graph(pattern: Pattern):
    if isinstance(pattern, PatternLeaf):
        points = set()
        edges = set()
        p = Pt(0, 0)
        points.add(p)
        for c in pattern.string:
            q = p + deltas[c]
            edges.add(tuple(sorted([p, q])))
            points.add(q)
            p = q
        return points, edges, {p}
    elif isinstance(pattern, PatternBranch):
        points = set()
        edges = set()
        endpoints = set()
        for child in pattern.children:
            child_points, child_edges, child_endpoints = build_graph(child)
            points |= child_points
            edges |= child_edges
            endpoints |= child_endpoints
        return points, edges, endpoints
    elif isinstance(pattern, PatternJoin):
        points = set()
        edges = set()
        endpoints = {Pt(0, 0)}
        for child in pattern.children:
            child_points, child_edges, child_endpoints = build_graph(child)
            updated_endpoints = set()
            for p in endpoints:
                points |= set(p + q for q in child_points)
                edges |= set((e0 + p, e1 + p) for e0, e1 in child_edges)
                updated_endpoints |= set(p + q for q in child_endpoints)
            endpoints = updated_endpoints
        return points, edges, endpoints


def draw_graph(points, edges):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    print("#" * (2 * abs(max_x - min_x + 1)) + "#")
    for x in range(min_x, max_x + 1):
        below_line = "#"
        line = "#"
        for y in range(min_y, max_y + 1):
            p = Pt(x, y)
            c = "X" if p == Pt(0, 0) else "."
            adj_edges = {}
            for k, v in deltas.items():
                q = p + v
                adj_edges[k] = tuple(sorted([p, q]))
            if adj_edges["S"] in edges:
                below_line += "-#"
            else:
                below_line += "##"
            if adj_edges["E"] in edges:
                line += c + "|"
            else:
                line += c + "#"
        print(line)
        print(below_line)


def main():
    tests = [
        "inputs/day20"
    ]
    for path in tests:
        with open(path) as f:
            for line in f:
                regex = line.strip()
                root = build_expression_tree(iter(regex), None)
                points, edges, endpoints = build_graph(root)
                print(max(distances(Pt(0, 0), edges)))
                print(len(list(filter(lambda d: d[0] >= 1000, distances(Pt(0, 0), edges)))))


if __name__ == "__main__":
    main()
