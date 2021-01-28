import collections
import itertools


def cell_power(x, y, serial):
    rack_id = x + 10
    power = ((rack_id * y) + serial) * rack_id
    return ((power % 1000) // 100) - 5


def max_power(sat, grid_size, n):
    return max(
        (sat[(x, y)] - sat[(x + n, y)] - sat[(x, y + n)] + sat[x + n, y + n], (x, y), n)
        for x, y in itertools.product(range(grid_size - n + 1), repeat=2)
    )


def main():
    grid_size = 300
    serial = 7347
    grid = {
        (x, y): cell_power(x + 1, y + 1, serial)
        for x, y in itertools.product(range(grid_size), repeat=2)
    }

    sat = collections.defaultdict(int)
    for i in reversed(range(0, grid_size)):
        for j in reversed(range(0, grid_size)):
            sat[(i, j)] = grid[(i, j)] + sat[(i + 1, j)] + sat[(i, j + 1)] - sat[(i + 1, j + 1)]
    power_p1, (x, y), n = max_power(sat, grid_size, 3)
    print("{},{}".format(x + 1, y + 1))

    power_p2, (x, y), square = max(
        max_power(sat, grid_size, n)
        for n in range(1, 301)
    )
    print("{},{},{}".format(x + 1, y + 1, square))


if __name__ == "__main__":
    main()
