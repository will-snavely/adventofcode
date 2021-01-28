import collections


def digits(n):
    result = collections.deque()
    while True:
        n, r = divmod(n, 10)
        result.appendleft(r)
        if n == 0:
            return result


def part1(threshold, number_after):
    recipes = [3, 7]
    elves = [0, 1]
    while True:
        if len(recipes) >= threshold + number_after:
            return "".join(str(n) for n in recipes[threshold:threshold + number_after])
        new_recipe = sum(recipes[i] for i in elves)
        recipes.extend(digits(new_recipe))
        for i in range(len(elves)):
            elves[i] = (elves[i] + recipes[elves[i]] + 1) % len(recipes)


def part2(pattern):
    recipes = [3, 7]
    elves = [0, 1]
    while True:
        new_recipe = sum(recipes[i] for i in elves)
        extension = digits(new_recipe)
        recipes.extend(extension)
        for i in range(len(extension)):
            start = len(recipes) - len(pattern) - i
            end = start + len(pattern)
            if tuple(recipes[start:end]) == pattern:
                return start
        for i in range(len(elves)):
            elves[i] = (elves[i] + recipes[elves[i]] + 1) % len(recipes)


def main():
    print(part1(640441, 10))
    print(part2((6, 4, 0, 4, 4, 1)))


if __name__ == "__main__":
    main()
