import functools

import pyparsing as pp

test_inputs = [
    "inputs/day16_sample",
    "inputs/day16",
]

Integer = pp.Word(pp.nums).setParseAction(pp.tokenMap(int))
ValidationRange = pp.Group(Integer("start") + pp.Suppress("-") + Integer("end"))
ValidationExpression = ValidationRange + pp.ZeroOrMore(pp.Suppress("or") + ValidationRange)
FieldName = pp.OneOrMore(pp.Word(pp.alphas))("name")
ValidationRule = pp.Group(FieldName("name") + pp.Suppress(":") + ValidationExpression("ranges"))
NumberList = pp.Group(Integer + pp.ZeroOrMore(pp.Suppress(",") + Integer))
YourTicket = pp.Literal("your ticket:")
NearbyTickets = pp.Literal("nearby tickets:")
Specification = pp.OneOrMore(ValidationRule)("rules") \
                + pp.Group(YourTicket + NumberList("values"))("yours") \
                + pp.Group(NearbyTickets + pp.Group(pp.ZeroOrMore(NumberList))("values"))("nearby")


class Range:
    def __init__(self, name, start, end):
        assert start <= end
        self.name = name
        self.start = start
        self.end = end

    def contains(self, value):
        return self.start <= value <= self.end


def process(path):
    print("Input:", path)
    with open(path) as f:
        contents = str(f.read())
        parsed = Specification.parseString(contents)
        rules = parsed["rules"]
        ranges = []
        ranges_by_field = {}
        for rule in rules:
            name = " ".join(rule["name"])
            ranges_by_field[name] = []
            for r in rule["ranges"]:
                range_obj = Range(name, r["start"], r["end"])
                ranges.append(range_obj)
                ranges_by_field[name].append(range_obj)

        nearby_tickets = parsed["nearby"]
        invalid_values = []
        valid_tickets = []
        for ticket_values in nearby_tickets["values"]:
            valid = True
            for value in ticket_values:
                if not any(r.contains(value) for r in ranges):
                    valid = False
                    invalid_values.append(value)
            if valid:
                valid_tickets.append(ticket_values)
        print("\tError Rate:", sum(invalid_values))

        possible_fields = {}
        for ticket in valid_tickets:
            for idx, value in enumerate(ticket):
                possible_set = set()
                for field, ranges in ranges_by_field.items():
                    if any(r.contains(value) for r in ranges):
                        possible_set.add(field)
                if idx in possible_fields:
                    possible_fields[idx] = possible_fields[idx].intersection(possible_set)
                else:
                    possible_fields[idx] = possible_set

        while True:
            determined = []
            for idx, possible in possible_fields.items():
                if len(possible) == 1:
                    determined.append(list(possible)[0])

            removed = False
            for idx, possible in possible_fields.items():
                if len(possible) > 1:
                    for d in determined:
                        if d in possible:
                            possible.remove(d)
                            removed = True

            if not removed:
                break

        your_ticket = parsed["yours"]["values"]
        departure_fields = []
        for idx, possible in possible_fields.items():
            if len(possible) != 1:
                print("Failed to determine field at index", idx)
                continue
            name = list(possible)[0]
            if name.startswith("departure"):
                departure_fields.append(your_ticket[idx])

        if departure_fields:
            print("\tDeparture Product:", functools.reduce(lambda x, y: x * y, departure_fields))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
