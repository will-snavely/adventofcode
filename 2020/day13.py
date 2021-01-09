test_inputs = [
    "inputs/day13_sample",
    "inputs/day13",
]

# Python 3.6
from functools import reduce


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def process(path):
    print("Input:", path)
    with open(path) as f:
        departure = int(f.readline())
        routes_raw = f.readline().strip().split(",")
        routes = [int(r) for r in routes_raw if r != "x"]
        dists = list(zip(routes, [(departure % x) - x for x in routes]))
        closest = max(dists, key=lambda x: x[1])
        print(closest[0] * abs(closest[1]))

        mod = 0
        a = []
        n = []
        N = 1
        for val in routes_raw:
            if val != "x":
                route = int(val)
                a.append(route - mod)
                n.append(route)
                N *= route
            mod += 1

        cr = chinese_remainder(n, a)
        print(n, a, N, cr)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
