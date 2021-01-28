import collections
import re

test_inputs = [
    "inputs/day9"
]

line_pattern = re.compile(r"(\d+)\s+players.*worth\s+(\d+)\s+points.*")


class LinkedNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def part1(players, marbles):
    current = LinkedNode(0)
    current.left = current.right = current
    player = 0
    scores = collections.defaultdict(int)
    for i in range(1, marbles + 1):
        if i % 23 == 0:
            remove = current
            for _ in range(7):
                remove = remove.left
            pred = remove.left
            succ = remove.right
            pred.right = succ
            succ.left = pred
            scores[player] += i + remove.value
            current = succ
        else:
            pred = current.right
            succ = current.right.right
            insert = LinkedNode(i, left=pred, right=succ)
            succ.left = insert
            pred.right = insert
            current = insert
        player = (player + 1) % players

    return scores


def process(path):
    with open(path) as f:
        for line in f:
            match = line_pattern.match(line)
            if match:
                players = int(match.group(1))
                marbles = int(match.group(2))
                scores = part1(players, marbles)
                print(play_game(players, marbles))
                print(play_game(players, marbles))
                scores = part1(players, marbles * 100)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
