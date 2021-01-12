import collections
import functools

test_inputs = [
    "inputs/day21_sample",
    "inputs/day21",
]


class Rule:
    def __init__(self, allergens, ingredients):
        self.allergens = set(allergens)
        self.ingredients = set(ingredients)


def iterate(rules, ingredient_universe, allergen_universe):
    by_allergen = collections.defaultdict(list)
    for r in rules:
        if r.allergens and r.ingredients:
            key = tuple(r.allergens)
            by_allergen[key].append(r.ingredients)

    facts = collections.defaultdict(lambda: ingredient_universe)
    for allergens, ingredient_sets in by_allergen.items():
        facts[allergens] = functools.reduce(lambda s, t: s & t, ingredient_sets)

    solutions = []
    for allergen in allergen_universe:
        relevant = [s for s in facts if allergen in s]
        if relevant:
            isect = functools.reduce(lambda s, t: s & t, [facts[r] for r in relevant])
            if len(isect) == 1:
                solutions.append((allergen, next(iter(isect))))

    return solutions


def process(path):
    print("Input:", path)
    with open(path) as f:
        rules = []
        ingredient_universe = set()
        allergen_universe = set()
        for line in f:
            line = line.replace("(", "").replace(")", "").replace(",", "")
            raw_ingredients, raw_allergies = line.split("contains")
            ingredients = set(raw_ingredients.strip().split())
            allergens = set(raw_allergies.strip().split())
            ingredient_universe = ingredient_universe | ingredients
            allergen_universe = allergen_universe | allergens
            rules.append(Rule(allergens, ingredients))

        all_solutions = []
        while True:
            solns = iterate(rules, ingredient_universe, allergen_universe)
            if solns:
                all_solutions = all_solutions + solns
                for allergen, ingredient in solns:
                    for rule in rules:
                        rule.allergens = rule.allergens - {allergen}
                        rule.ingredients = rule.ingredients - {ingredient}
            else:
                break

        count = 0
        for rule in rules:
            count += len(rule.ingredients)
        print("\tPart 1:", count)
        print("\tPart 2:", ",".join([s[1] for s in sorted(all_solutions)]))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
