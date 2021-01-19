import itertools

from aoc2019.intcode import IntCodeProcess

test_inputs = [
    "inputs/day25"
]


def parse_output(output):
    room = ""
    description = ""
    exits = []
    items = []
    section = None
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("=="):
            room = line
            section = "room"
        elif line.startswith("Doors here lead:"):
            section = "exits"
        elif line.startswith("Items here:"):
            section = "items"
        elif line.startswith("Command?"):
            continue
        else:
            if section == "room":
                description += line
            elif section == "exits":
                exits.append(line.strip("-").strip())
            elif section == "items":
                items.append(line.strip("-").strip())
    return room, description, exits, items


def encode(command):
    command = command.strip() + "\n"
    return [ord(x) for x in command]


deltas = {
    "north": (0, 1),
    "south": (0, -1),
    "east": (1, 0),
    "west": (-1, 0)
}

reverse = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east"
}


def collect(seen, controller, entry_command, unsafe_items):
    if entry_command:
        controller.send(*encode(entry_command))
    controller.run()
    output = "".join([chr(x) for x in controller.flush()])
    room, desc, exits, items = parse_output(output)
    if room not in seen:
        seen.add(room)
        for item in items:
            if item in unsafe_items:
                continue
            take_command = "take {}".format(item)
            controller.send(*encode(take_command))
            controller.run()
            take_result = "".join([chr(x) for x in controller.flush()])
            if "Command?" not in take_result:
                print("Unknown unsafe item?")
                print(take_result)
                exit()

        if "Security Checkpoint" not in room:
            for e in exits:
                if entry_command is None or e != reverse[entry_command]:
                    collect(seen, controller, e, unsafe_items)
    if entry_command:
        controller.send(*encode(reverse[entry_command]))
        controller.run()
        controller.flush()


def try_item_combos(controller, items):
    for n in range(len(items)):
        for attempt in itertools.combinations(items, n):
            keep = set(attempt)
            drop = items - keep
            for item in drop:
                command = "drop {}".format(item)
                controller.send(*encode(command))
                controller.run()
                controller.flush()
            move = "south"
            controller.send(*encode(move))
            controller.run()
            output = "".join([chr(x) for x in controller.flush()])

            if "You may proceed" in output:
                print(keep, output)
                return

            for item in drop:
                command = "take {}".format(item)
                controller.send(*encode(command))
                controller.run()
                controller.flush()


def part1(path):
    safe_items = {
        "hypercube",
        "coin",
        "klein bottle",
        "shell",
        "easter egg",
        "astrolabe",
        "tambourine",
        "dark matter"
    }
    unsafe_items = {
        "photons",
        "giant electromagnet",
        "molten lava",
        "escape pod",
        "infinite loop"
    }
    controller = IntCodeProcess.compile(path)
    collect(set(), controller, None, unsafe_items)
    travel = ["west", "west", "north", "west", "south"]
    for cmd in travel:
        controller.send(*encode(cmd))
        controller.run()
        controller.flush()
    try_item_combos(controller, safe_items)


def process(path):
    part1(path)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
