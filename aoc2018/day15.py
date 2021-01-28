import copy
import itertools
from collections import defaultdict, deque

deltas = {(-1, 0), (0, -1), (1, 0), (0, 1)}


class DeadElfError(Exception):
    pass


class Creature:
    def __init__(self, symbol, hp=200):
        self.hp = hp
        self.symbol = symbol

    def alive(self):
        return self.hp > 0

    def __repr__(self):
        return "{}[{}]".format(self.symbol, self.hp)


class Dungeon:
    def __init__(self):
        self.floor = set()
        self.creatures = {}
        self.height = 0
        self.width = 0
        self.power = {"G": 3, "E": 3}
        self.can_elves_die = True

    def draw(self):
        for row in range(self.height):
            line = ""
            seen = []
            for col in range(self.width):
                p = (row, col)
                if p in self.creatures:
                    line += self.creatures[p].symbol
                    seen.append(p)
                else:
                    line += "." if p in self.floor else "#"
            for p in seen:
                line += " {}@{}".format(self.creatures[p], p)
            print(line)

    def tick(self):
        work_list = [
            (p, self.creatures[p])
            for p in sorted(self.creatures.keys())
        ]

        for pos, cur in work_list:
            if not cur.alive():
                continue

            enemy = "E" if cur.symbol == "G" else "G"
            targets = [
                p for p in self.creatures
                if self.creatures[p].symbol == enemy
            ]
            if not targets:
                return False

            attack_options = self.adjacent_creatures(pos, enemy)
            if not attack_options:
                in_range = set(
                    itertools.chain.from_iterable((self.adjacent_empty(p) for p in targets))
                )
                move_options = defaultdict(lambda: defaultdict(list))
                min_dist = None
                for p in self.adjacent_empty(pos):
                    options, min_dist = self.pathfind(p, in_range, limit=min_dist)
                    for opt in options:
                        move_options[min_dist][opt].append(p)

                if move_options:
                    destination = min(move_options[min_dist].keys())
                    new_position = min(move_options[min_dist][destination])
                    del self.creatures[pos]
                    self.creatures[new_position] = cur
                    attack_options = self.adjacent_creatures(new_position, enemy)

            if attack_options:
                by_hp = defaultdict(list)
                for p in attack_options:
                    by_hp[self.creatures[p].hp].append(p)
                min_hp = min(by_hp)
                target = min(by_hp[min_hp])
                self.damage(target, self.power[cur.symbol])

        return True

    def damage(self, target, amt):
        creature = self.creatures.get(target)
        creature.hp -= amt
        if not creature.alive():
            if not self.can_elves_die and creature.symbol == "E":
                raise DeadElfError()
            del self.creatures[target]

    def pathfind(self, start, targets, limit=None):
        if not targets:
            return [], limit
        queue = deque()
        queue.append((start, 0))
        seen = {start}
        reachable = []
        while queue:
            p, dist = queue.popleft()
            if p in targets:
                if limit is None or dist <= limit:
                    reachable.append(p)
                    limit = dist
            for n in self.adjacent_empty(p):
                if n not in seen and (limit is None or dist < limit):
                    seen.add(n)
                    queue.append((n, dist + 1))
        return reachable, limit

    def adjacent_empty(self, pos):
        points = ((pos[0] + d[0], pos[1] + d[1]) for d in deltas)
        return [
            p for p in points
            if p in self.floor and p not in self.creatures
        ]

    def adjacent_creatures(self, pos, kind):
        points = ((pos[0] + d[0], pos[1] + d[1]) for d in deltas)
        return [
            p for p in points
            if p in self.creatures and self.creatures[p].symbol == kind
        ]


def build_dungeon(path):
    dungeon = Dungeon()
    creatures = set("GE")
    for row, line in enumerate(open(path)):
        dungeon.height += 1
        dungeon.width = max(dungeon.width, len(line.strip()))
        for col, char in enumerate(line):
            if char == ".":
                dungeon.floor.add((row, col))
            elif char in creatures:
                dungeon.floor.add((row, col))
                dungeon.creatures[(row, col)] = Creature(char)
    return dungeon


def simulate(dungeon):
    round_number = 0
    while dungeon.tick():
        round_number += 1
    total_hp = sum([c.hp for c in dungeon.creatures.values() if c.alive()])
    return round_number, total_hp, round_number * total_hp


def part2(base_dungeon):
    elf_power = 4
    while True:
        fork = copy.deepcopy(base_dungeon)
        fork.power["E"] = elf_power
        fork.can_elves_die = False
        try:
            return simulate(fork), elf_power
        except DeadElfError:
            elf_power += 1


def main():
    tests = [
        ("inputs/day15_test1", 37, 982, 36334),
        ("inputs/day15_test2", 47, 590, 27730),
        ("inputs/day15_test3", 46, 859, 39514),
        ("inputs/day15_test4", 20, 937, 18740),
        ("inputs/day15_test5", 54, 536, 28944),
        ("inputs/day15_test6", 35, 793, 27755),
        ("inputs/day15", 126, 2535, 319410),
    ]
    for test in tests:
        path, expected_round, expected_sum, expected_score = test
        print(path)
        dungeon = build_dungeon(path)
        round_number, hp_sum, score = simulate(copy.deepcopy(dungeon))
        print("\tPart1:", round_number, hp_sum, score)
        assert round_number == expected_round
        assert hp_sum == expected_sum
        assert score == expected_score

        (round_number, hp_sum, score), elf_power = part2(dungeon)
        print("\tPart2:", elf_power, round_number, hp_sum, score)


if __name__ == "__main__":
    main()
