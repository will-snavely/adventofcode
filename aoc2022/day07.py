class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.size = 0
        self.parent = parent
        self.dirs = {}
        self.files = {}

    def add_dir(self, name):
        if name not in self.dirs:
            self.dirs[name] = Dir(name, self)

    def add_file(self, name, size):
        self.files[name] = File(name, size)

def compute_dir_sizes(tree):
    tree.size = 0
    for file in tree.files.values():
        tree.size += file.size

    for dr in tree.dirs.values():
        compute_dir_sizes(dr)
        tree.size += dr.size

def sum_smaller_than(tree, thresh):
    result = 0
    if tree.size <= thresh:
        result += tree.size

    for dr in tree.dirs.values():
        result += sum_smaller_than(dr, thresh)

    return result

def find_best_delete(tree, target):
    best = tree
    for dr in tree.dirs.values():
        if dr.size > target:
            res = find_best_delete(dr, target)
            if res.size < best.size:
                best = res
    return best

if __name__ == "__main__":
    with open("inputs/day07") as f:
        root = Dir("<root>", None)
        cur = root
        commands = [x.strip() for x in f.readlines()]
        for cmd in commands:
            match cmd.split():
                case ['$', 'cd', ".."]:
                    cur = cur.parent
                case ['$', 'cd', name]:
                    cur.add_dir(name)
                    cur = cur.dirs[name]
                case ['$', 'ls']:
                    pass
                case ["dir", name]:
                    cur.add_dir(name)
                case [size, name]:
                    cur.add_file(name, int(size))
        compute_dir_sizes(root)
        p1_threshold = 100000
        print(sum_smaller_than(root.dirs["/"], p1_threshold))

        cap = 70000000
        free = cap - root.size
        needed = 30000000 - free
        best = find_best_delete(root, needed)
        print(best.name, best.size)
