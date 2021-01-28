test_inputs = [
    "inputs/day8"
]


class Tree:
    def __init__(self):
        self.children = []
        self.metadata = []


def build(data, index):
    children_len = data[index]
    metadata_len = data[index + 1]
    child_index = index + 2
    parent = Tree()
    for _ in range(children_len):
        child, size = build(data, child_index)
        parent.children.append(child)
        child_index += size
    parent.metadata.extend(data[child_index:child_index + metadata_len])
    return parent, child_index + metadata_len - index


def sum_metadata(tree: Tree):
    return sum(tree.metadata) + sum(sum_metadata(c) for c in tree.children)


def find_value(tree: Tree):
    if len(tree.children) == 0:
        return sum(tree.metadata)
    cache = {}
    result = 0
    for meta in tree.metadata:
        if meta < 1 or meta > len(tree.children):
            continue
        if meta not in cache:
            cache[meta] = find_value(tree.children[meta - 1])
        result += cache[meta]
    return result


def process(path):
    with open(path) as f:
        data = [int(x) for x in f.read().split()]
        root, size = build(data, 0)
        print(sum_metadata(root))
        print(find_value(root))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
