import collections
import math

test_inputs = [
    "inputs/day14"
]


def parse_line(line):
    l, r = line.strip().split("=>")
    raw_ingredients = l.strip().split(",")
    ingredients = []
    for ri in raw_ingredients:
        parts = ri.split()
        ingredients.append((int(parts[0]), parts[1].strip()))
    out_parts = r.split()
    output = (int(out_parts[0]), out_parts[1].strip())
    return ingredients, output


def traverse(graph, node, amount, requested, produced):
    if node == "ORE" or amount == 0:
        requested[node] += amount
        produced[node] += amount
        return

    qty, recipe = graph[node]
    extra = produced[node] - requested[node]
    repeat = math.ceil((amount - extra) / qty)
    requested[node] += amount
    produced[node] += repeat * qty

    for ingredient_qty, ingredient in recipe:
        traverse(graph, ingredient, ingredient_qty * repeat, requested, produced)


def make_fuel(amt, recipe_graph):
    requested = collections.defaultdict(int)
    produced = collections.defaultdict(int)
    traverse(recipe_graph, "FUEL", amt, requested, produced)
    return requested, produced


def search(recipe_graph, ore_amount, start, delta):
    fuel_target = start
    while True:
        req, prod = make_fuel(fuel_target, recipe_graph)
        if prod["ORE"] >= ore_amount:
            return fuel_target
        fuel_target += delta


def process(path):
    with open(path) as f:
        graph = {}
        for line in f:
            ingredients, output = parse_line(line)
            graph[output[1]] = (output[0], ingredients)
        requested, produced = make_fuel(1, graph)
        print("ORE needed:", produced["ORE"])

        ore_amount = 1000000000000
        start = 0
        deltas = [10 ** e for e in reversed(range(8))]
        for delta in deltas:
            result = search(graph, ore_amount, start, delta)
            start = result - delta
        print("FUEL possible:", start)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
