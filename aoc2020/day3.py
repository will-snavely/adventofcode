import functools


def count_trees(forest, start_row, start_col, dr, dc):
    row = start_row
    col = start_col

    tree_count = 0
    while row < len(forest):
        cell = forest[row][col]
        if cell == "#":
            tree_count += 1

        col = (col + dc) % len(forest[row])
        row += dr
    return tree_count


if __name__ == "__main__":
    with open("inputs/day3") as f:
        forest = list()
        for line in f:
            forest.append(line.strip())
        print(count_trees(forest, 0, 0, 1, 3))

        part2 = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        results = [count_trees(forest, 0, 0, dr, dc) for (dc, dr) in part2]
        print(results)
        print(functools.reduce(lambda a, b: a * b, results))
