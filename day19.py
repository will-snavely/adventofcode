import functools

from pyparsing import (
    ZeroOrMore, OneOrMore, Word, Suppress, Forward, Group, tokenMap, nums, alphas, Literal
)

test_inputs = [
    "inputs/day19_part2"
]

Integer = Word(nums).setParseAction(tokenMap(int))
CharacterExpr = Suppress("\"") + Word(alphas, exact=1) + Suppress("\"")
RuleRefSeq = OneOrMore(Integer, stopOn="\n")
RuleRefExpr = Group(RuleRefSeq) + ZeroOrMore(Suppress("|") + Group(RuleRefSeq))
RuleExpr = CharacterExpr("char") | RuleRefExpr("subrules")
Rule = Integer("index") + Suppress(":") + RuleExpr("value")
Message = Word(alphas)
Line = Rule("rule") | Message("message")


def build_grammar(rules):
    grammar = {}
    for rule in rules:
        grammar[rule["index"]] = Forward()

    for rule in rules:
        index = rule["index"]
        if "char" in rule:
            grammar[index] << (Literal(rule["value"][0]))
        else:
            subrules = rule["subrules"]
            summed_rules = [
                functools.reduce(lambda a, b: a + b, [grammar[idx] for idx in group])
                for group in subrules
            ]
            grammar[index] << functools.reduce(
                lambda a, b: a ^ b,
                summed_rules
            )
    return grammar


def process(path):
    print("Input:", path)
    with open(path) as f:
        rules = []
        messages = []
        for line in f:
            if line.strip():
                spec = Line.parseString(line)
                if "rule" in spec:
                    rules.append(spec)
                else:
                    messages.append(spec[0])
    grammar = build_grammar(rules)
    valid = []
    invalid = []
    part_2_grammar = Group(OneOrMore(Group(grammar[42]))) + Group(OneOrMore(Group(grammar[31])))
    for message in messages:
        try:
            result = part_2_grammar.parseString(message, parseAll=True)
            if len(result[1]) < len(result[0]):
                valid.append(message)
        except:
            invalid.append(message)
    print("\tNumber Valid:", len(valid))
    print(valid)
    print(invalid)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
