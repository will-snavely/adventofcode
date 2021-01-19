test_inputs = [
    "inputs/day18_sample",
    "inputs/day18_part1",
]

nums = set("0123456789")
ws = set("\t\n\r ")
op = set("+*")


def tokenize(line):
    num_buffer = ""
    for c in line:
        if c in nums:
            num_buffer += c
        else:
            if num_buffer != "":
                yield "number", int(num_buffer)
                num_buffer = ""
            if c in op:
                yield "op", c
            elif c == "(":
                yield "lparen", c
            elif c == ")":
                yield "rparen", c
    if num_buffer != "":
        yield "number", int(num_buffer)


def evaluate(postfix):
    stack = list()
    for token in postfix:
        if token == "+":
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 + op2)
        elif token == "*":
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 * op2)
        else:
            stack.append(token)
    return stack.pop()


def to_postfix(infix_tokens, precedence):
    result = []
    opstack = []

    for kind, token in infix_tokens:
        if kind == "number":
            result.append(token)
        elif kind == "lparen":
            opstack.append("(")
        elif kind == "rparen":
            while True:
                top = opstack.pop()
                if top == "(":
                    break
                else:
                    result.append(top)
        elif kind == "op":
            op_prec = precedence[token]
            done = False
            while not done and len(opstack) > 0:
                top = opstack[-1]
                if top != "(" and precedence[top] >= op_prec:
                    result.append(opstack.pop())
                else:
                    done = True
            opstack.append(token)
    while len(opstack) > 0:
        result.append(opstack.pop())

    return result


def process(path):
    print("Input:", path)
    with open(path) as f:
        sum_p1 = 0
        sum_p2 = 0
        for line in f:
            tokens = list(tokenize(line))
            postfix_p1 = to_postfix(tokens, {"+": 0, "*": 0})
            postfix_p2 = to_postfix(tokens, {"+": 1, "*": 0})
            sum_p1 += evaluate(postfix_p1)
            sum_p2 += evaluate(postfix_p2)
        print("\tSum Part 1:", sum_p1)
        print("\tSum Part 2:", sum_p2)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
