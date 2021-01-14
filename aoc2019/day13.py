from aoc2019.intcode import IntCodeProcess

test_inputs = [
    "inputs/day13"
]


class Game:
    def __init__(self):
        self.screen = {}
        self.score = None
        self.ball_position = None
        self.paddle_position = None


def update(game: Game, output):
    for idx in range(0, len(output), 3):
        x, y, c = output[idx:idx + 3]
        if x == -1 and y == 0:
            game.score = c
        else:
            game.screen[(x, y)] = c

    for pos, c in game.screen.items():
        if c == 4:
            game.ball_position = pos
        elif c == 3:
            game.paddle_position = pos


def draw(game, width, height):
    symbols = {
        0: " ",
        1: "#",
        2: "+",
        3: "-",
        4: "o"
    }
    for y in range(0, height + 1):
        row = ""
        for x in range(0, width + 1):
            if (x, y) in game.screen:
                row += symbols[game.screen[(x, y)]]
            else:
                row += " "
        print(row)


def process(path):
    print("Input:", path)

    with open(path) as f:
        program = [int(x) for x in f.readline().split(",")]

    game = Game()
    proc = IntCodeProcess(program)
    proc.memory[0] = 2
    while not proc.done():
        proc.run()
        output = proc.flush()
        update(game, output)
        # draw(game, 40, 20)
        if game.ball_position[1] == 19:
            proc.memory[392] = game.ball_position[0] - 1
            proc.send(1)
        else:
            proc.send(0)
    print(game.ball_position, game.paddle_position, game.score)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
